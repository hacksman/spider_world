#!/usr/bin/env python 
# coding:utf-8

import types
import math
import asyncio

from tqdm import tqdm


class Downloader(object):

    def __init__(self, handlers=[], batch=10):
        self.handlers = handlers
        self.batch = batch

    def set_handlers(self, handlers):
        self.handlers = handlers

    def add_handlers(self, handler):
        self.handlers.append(handler)

    def get_handlers(self):

        return self.handlers

    async def process_item(self, obj):

        raise NotImplementedError

    def update_process(self, _):
        self.bar.update(1)

    def process_items(self, objs):
        with tqdm(total=len(objs)) as self.bar:

            loop = asyncio.get_event_loop()
            total_steps = int(math.ceil(len(objs) / self.batch))

            for step in range(total_steps):
                start, end = step * self.batch, (step + 1) * self.batch
                objs_batch = objs[start:end]
                print("Process...<{}>-<{}> of files".format(start + 1, end))
                tasks = [asyncio.ensure_future(self.process_item(_)) for _ in objs_batch]
                for task in tasks:
                    task.add_done_callback(self.update_process)
                loop.run_until_complete(asyncio.wait(tasks))

    def download(self, inputs):
        if isinstance(inputs, types.GeneratorType):
            temps = []
            for result in inputs:
                temps.append(result)
                if len(temps) >= self.batch:
                    self.process_items(temps)
            self.process_items(temps)
        else:
            self.process_items(inputs) if isinstance(inputs, list) else self.process_items([inputs])

