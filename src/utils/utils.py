"""
Utils module for common functions and utilities
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import functools


async def run_in_process(fn, *args, **kwargs):
    """
    Asynchronously runs the given function in a separate process using ProcessPoolExecutor

    Args:
        fn (function): The function to run in a separate process
        *args (Any): The arguments to be passed to the function
        **kwargs (Any): The keyword arguments to be passed to the function

    Returns:
        Any: The result of the function run in the separate process
    """
    # Create a ProcessPoolExecutor instance
    with ProcessPoolExecutor() as executor:
        # Get the event loop
        loop = asyncio.get_event_loop()
        # Partially apply the function with the given arguments
        partial_fn = functools.partial(fn, *args, **kwargs)
        # Run the function in the executor and wait for it to complete
        return await loop.run_in_executor(executor, partial_fn)


async def run_in_thread(fn, *args, **kwargs):
    """
    Asynchronously runs the given function in a separate thread using ThreadPoolExecutor.

    Args:
        fn (function): The function to run in a separate thread.
        *args (Any): The arguments to be passed to the function.
        **kwargs (Any): The keyword arguments to be passed to the function.

    Returns:
        Any: The result of the function run in the separate thread.
    """
    # Create a ThreadPoolExecutor instance.
    with ThreadPoolExecutor() as executor:
        # Get the event loop.
        loop = asyncio.get_event_loop()
        # Partially apply the function with the given arguments.
        partial_fn = functools.partial(fn, *args, **kwargs)
        # Run the function in the executor and wait for it to complete.
        return await loop.run_in_executor(executor, partial_fn)
