# Copied from https://git.io/fAGgA with small updates

import asyncio
import contextvars
import random
import unittest


class TaskTests(unittest.TestCase):
    def test_context_1(self):
        cvar = contextvars.ContextVar('cvar')

        async def sub():
            await asyncio.sleep(0.01, loop=loop)
            self.assertEqual(cvar.get(), 'nope')
            cvar.set('something else')

        async def main():
            cvar.set('nope')
            self.assertEqual(cvar.get(), 'nope')
            subtask = loop.create_task(sub())
            cvar.set('yes')
            self.assertEqual(cvar.get(), 'yes')
            await subtask
            self.assertEqual(cvar.get(), 'yes')

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(main())
        finally:
            loop.close()

    def test_context_2(self):
        cvar = contextvars.ContextVar('cvar', default='nope')

        async def main():
            def fut_on_done(fut):
                # This change must not pollute the context
                # of the "main()" task.
                cvar.set('something else')

            self.assertEqual(cvar.get(), 'nope')

            for j in range(2):
                fut = loop.create_future()
                ctx = contextvars.copy_context()
                fut.add_done_callback(lambda f: ctx.run(fut_on_done, f))
                cvar.set('yes{}'.format(j))
                loop.call_soon(fut.set_result, None)
                await fut
                self.assertEqual(cvar.get(), 'yes{}'.format(j))

                for i in range(3):
                    # Test that task passed its context to add_done_callback:
                    cvar.set('yes{}-{}'.format(i, j))
                    await asyncio.sleep(0.001, loop=loop)
                    self.assertEqual(cvar.get(), 'yes{}-{}'.format(i, j))

        loop = asyncio.new_event_loop()
        try:
            task = loop.create_task(main())
            loop.run_until_complete(task)
        finally:
            loop.close()

        self.assertEqual(cvar.get(), 'nope')

    def test_context_3(self):
        # Run 100 Tasks in parallel, each modifying cvar.

        cvar = contextvars.ContextVar('cvar', default=-1)

        async def sub(num):
            for i in range(10):
                cvar.set(num + i)
                await asyncio.sleep(
                    random.uniform(0.001, 0.05), loop=loop)
                self.assertEqual(cvar.get(), num + i)

        async def main():
            tasks = []
            for i in range(100):
                task = loop.create_task(sub(random.randint(0, 10)))
                tasks.append(task)

            await asyncio.gather(*tasks, loop=loop)

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(main())
        finally:
            loop.close()

        self.assertEqual(cvar.get(), -1)
