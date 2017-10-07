import os
from unittest import mock
from datetime import datetime

from ...testing import TestCase
from ..process import (
    TaskBase,
    Process,
    Task)


class TaskBaseTests(TestCase):

    def setUp(self):
        super().setUp()
        self.id = 10
        self.task = TaskBase(
            self.id, os.path.join(self.tempdir.path, str(self.id)))

    def test_repr(self):
        """__repr__ includes the task ID."""
        self.assertEqual(repr(self.task), 'TaskBase(10)')

    def test_id(self):
        """The id attribute returns the task identifier."""
        self.assertEqual(self.task._id, self.id)

    def test_exists(self):
        """It's possible to check whether a process exists."""
        self.assertFalse(self.task.exists)
        self.make_process_file(self.id, 'cmdline', content='cmd')
        self.assertTrue(self.task.exists)

    def test_collect_stats(self):
        """Stats are collected from proc when collect_stats is called."""
        self.assertEqual([], self.task.available_stats())
        self.make_process_file(self.id, 'cmdline', content='cmd')
        self.task.collect_stats()
        self.assertEqual(self.task.available_stats(), ['cmdline'])

    def test_collect_stats_no_proc_dir(self):
        """If the task dir is not found, stats are left empty."""
        self.task.collect_stats()
        self.assertEqual(self.task.available_stats(), [])
        self.assertEqual(self.task.stats(), {})

    def test_collect_stats_prefix(self):
        """The file prefix is used if it reports multiple stats."""
        self.make_process_file(self.id, 'statm', content='1 2 3 4 5 6 7')
        self.task.collect_stats()
        self.assertEqual(
            self.task.stats(),
            {'statm.size': 1, 'statm.resident': 2, 'statm.share': 3,
             'statm.text': 4, 'statm.lib': 5, 'statm.data': 6, 'statm.dt': 7})

    def test_collect_stats_unreadable_file(self):
        """Unreadable files are skipped when reading stats."""
        self.make_process_file(self.id, 'cmdline', content='cmd', mode=0o200)
        self.task.collect_stats()
        self.assertEqual(self.task.available_stats(), [])

    def test_collect_stats_not_parsable(self):
        """STats are not collected for entries that are not parsable files."""
        self.make_process_dir(self.id, 'task')
        self.task.collect_stats()
        self.assertEqual(self.task.available_stats(), [])

    @mock.patch('lxstats.files.text.ParsedFile.parse')
    def test_collect_stats_ioerror(self, mock_file):
        """If reading a file raises an IOError, the stat is skipped."""
        self.make_process_file(self.id, 'cmdline', content='cmd')
        mock_file.side_effect = IOError()

        self.task.collect_stats()
        self.assertEqual(self.task.available_stats(), [])

    def test_cmd_from_cmdline(self):
        """TaskBase.cmd parses the content of cmdline if not empty."""
        self.make_process_file(
            self.id, 'cmdline', content='cmd\x00with\x00args\x00')
        self.task.collect_stats()
        self.assertNotIn('comm', self.task.available_stats())
        self.assertEqual(
            self.task.get('cmdline'), ['cmd', 'with', 'args'])
        self.assertEqual(self.task.cmd, 'cmd with args')

    def test_cmd_from_comm(self):
        """If cmdline is empty, comm is read."""
        self.make_process_file(self.id, 'comm', content='cmd')
        self.task.collect_stats()
        self.assertNotIn('cmdline', self.task.available_stats())
        self.assertEqual(self.task.cmd, '[cmd]')

    def test_cmd_empty(self):
        """If cmdline and cmd are not found, an empty string is returned."""
        self.task.collect_stats()
        self.assertEqual(self.task.cmd, '')

    def test_timestamp_empty(self):
        """The timestamp is None when stats have not been collected."""
        self.make_process_file(self.id, 'cmdline', content='cmd')
        self.assertIsNone(self.task.timestamp)

    def test_timestamp(self):
        """The timestamp is None when stats have not been collected."""
        self.make_process_file(self.id, 'cmdline', content='cmd')
        now = datetime.utcnow()
        self.task._utcnow = lambda: now
        self.task.collect_stats()
        self.assertEqual(self.task.timestamp, now)

    def test_available_stats(self):
        """Available Process stats can be listed."""
        self.make_process_file(self.id, 'comm', content='cmd')
        self.make_process_file(self.id, 'wchan', content='0')
        self.task.collect_stats()
        self.assertEqual(self.task.available_stats(), ['comm', 'wchan'])

    def test_stats(self):
        """Available Process  stats can be returned as a dict ."""
        self.make_process_file(self.id, 'comm', content='cmd')
        self.make_process_file(self.id, 'wchan', content='0')
        self.task.collect_stats()
        self.assertEqual(self.task.stats(), {'comm': 'cmd', 'wchan': '0'})

    def test_get(self):
        """Value for a stat can be returned."""
        self.make_process_file(
            self.id, 'wchan', content='poll_schedule_timeout')
        self.task.collect_stats()
        self.assertEqual(self.task.get('wchan'), 'poll_schedule_timeout')

    def test_get_not_found(self):
        """If the requested stat is not found, None is returned."""
        self.task.collect_stats()
        self.assertIsNone(self.task.get('wchan'))

    def test_get_cmd(self):
        """The get() method can return the cmd."""
        self.make_process_file(self.id, 'cmdline', content='cmd')
        self.task.collect_stats()
        self.assertEqual(self.task.get('cmd'), 'cmd')

    def test_equal(self):
        """Two Processes are equal if they have the same pid."""
        other = Process(
            self.id, '{}/{}'.format(self.tempdir.path, self.id))
        different = Process(
            self.id + 1, '{}/{}'.format(self.tempdir.path, self.id))
        self.assertEqual(self.task, other)
        self.assertNotEqual(self.task, different)


class ProcessTests(TestCase):

    def setUp(self):
        super().setUp()
        self.pid = 10
        self.process = Process(
            self.pid, os.path.join(self.tempdir.path, str(self.pid)))

    def test_pid(self):
        """The pid attribute returns the PID."""
        self.assertEqual(self.process.pid, self.pid)

    def test_get_pid(self):
        """The get() method can return the PID."""
        self.process.collect_stats()
        self.assertEqual(self.process.get('pid'), self.pid)

    def test_tasks(self):
        """The list of TIDs for process tasks can be returned."""
        self.make_process_dir(self.pid, 'task/123')
        self.make_process_dir(self.pid, 'task/456')
        self.assertCountEqual(
            self.process.tasks(),
            [Task(123, self, os.path.join(self.tempdir.path, 'task', '123')),
             Task(456, self, os.path.join(self.tempdir.path, 'task', '456'))])


class TaskTests(TestCase):

    def setUp(self):
        super().setUp()
        self.id = 10
        self.process = Process(
            self.id, '{}/{}'.format(self.tempdir.path, self.id))
        self.task = Task(
            self.id, self.process,
            '{}/{}/task/{}'.format(self.tempdir.path, self.id, self.id))

    def test_pid(self):
        """The tid attribute returns the TID."""
        self.assertEqual(self.task.tid, self.id)

    def test_process(self):
        """The parent attribute returns the task parent process."""
        self.assertEqual(self.task.parent, self.process)

    def test_get_pid(self):
        """The get() method can return the PID."""
        self.task.collect_stats()
        self.assertEqual(self.task.get('tid'), self.id)
