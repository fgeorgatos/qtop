from serialiser import *
import random
WORKER_NODES = 50
QUEUES = 3


class DemoBatchSystem(GenericBatchSystem):
    """
    This is an example implementation of how a batch system is "read" and what is expected of it
    by qtop in order to run.
    """

    @staticmethod
    def get_mnemonic():
        return "demo"

    def __init__(self, scheduler_output_filenames, config):
        """
        config corresponds to the QTOPCONF_YAML file distributed with qtop.
        Custom QTOPCONF files can be created and placed either
        in USERPATH/QTOPCONF_YAML or in SYSTEMCONFDIR/QTOPCONF_YAML
        """
        self.scheduler_output_filenames = scheduler_output_filenames
        self.config = config
        self.jobs = list()  # needed just for the demo to work
        self.total_nps = 0

    def get_worker_nodes(self):
        """
        Possible node states are:
        "-": free
        "b": busy
        "d": down/offline
        and generally the first letter of the word describing the state is used.
        """

        worker_nodes = list()
        for i in range(WORKER_NODES):
            worker_node = dict()
            worker_node["domainname"] = "".join([
                random.choice(['dn', 'pc', 'wn']),
                str(random.randint(0,10)),
                random.choice(['foo.com', 'bar.com', 'baz.com'])])
            worker_node["state"] = random.choice(["-", "b", "d"])
            worker_node["gpus"] = random.choice([0, 2, 4, 8, 16, 24, 32])
            worker_node["np"] = random.choice([8, 16, 24, 32])
            self.total_nps += worker_node["np"]

            # pick a series of random core/random job nr pairs
            worker_node["core_job_map"] = dict()
            for i in range(random.randint(0, worker_node["np"])):
                if worker_node["state"] == "d": break
                random_job_id = "j" + str(random.randint(0, 500))
                random_core = random.choice(range(worker_node["np"]))
                worker_node["core_job_map"][random_core] = random_job_id
                self.jobs.append(random_job_id)
            worker_nodes.append(worker_node)

        return worker_nodes

    def get_jobs_info(self):
        """
        These 4 lists have to be of the same length (TODO: maybe make a tuple out of them or consider an alternative structure?)
        """
        job_ids = self.jobs
        # These are used in the upper and lower parts of qtop in the statistics part
        job_states = [random.choice("Q R C E W".split()) for _ in job_ids]
        usernames = [random.choice("alice023 cmsmu lhc154 fotis Atlassm".split()) for _ in job_ids]
        queue_names = [random.choice("Urgent Foobar Urgent Foobar Priori".split()) for _ in job_ids]
        return job_ids, usernames, job_states, queue_names

    def get_queues_info(self):
        total_running_jobs = 110  # these are reported directly by qstat in PBS; if not, they are calculated.
        total_queued_jobs = 100

        qstatq_list = list()
        for i in range(QUEUES):
            qstatq = dict()
            qstatq['run'] = random.randint(0, 15)
            qstatq['queued'] = str(random.randint(0, 15))
            qstatq['queue_name'] = random.choice("Urgent Foobar Priori".split())
            qstatq['state'] = random.choice("Q R C E W".split())
            qstatq['lm'] = random.randint(0, 100)
            qstatq_list.append(qstatq)

        return total_running_jobs, total_queued_jobs, qstatq_list
