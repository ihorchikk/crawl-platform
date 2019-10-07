import logging


class Task:
    """
    Base class for some async task
    """
    def __init__(self):
        self.logger = logging.getLogger('tasks')

    async def __call__(self, *args, **kwargs):
        """
        Main method for running Task.
        """
        try:
            task_logic_result = await self.task_logic(*args, **kwargs)
            return task_logic_result
        except Exception as e:
            self.logger.error('There is exception during task execution: {}'.format(e))

    async def task_logic(self, *args, **kwargs):
        """
        Here we store the main logic of task.
        Override this method for each task
        """
        pass

