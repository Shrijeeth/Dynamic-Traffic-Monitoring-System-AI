"""
Utils module for common functions and utilities
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


async def run_in_process(fn, *args):
    """
    Asynchronously runs the given function in a separate process using ProcessPoolExecutor

    Args:
        fn (function): The function to run in a separate process
        *args (Any): The arguments to be passed to the function

    Returns:
        Any: The result of the function run in the separate process
    """
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, fn, *args)


async def run_in_thread(fn, *args):
    """
    Asynchronously runs the given function in a separate thread using ThreadPoolExecutor

    Args:
        fn (function): The function to run in a separate thread
        *args (Any): The arguments to be passed to the function

    Returns:
        Any: The result of the function run in the separate thread
    """
    with ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, fn, *args)
