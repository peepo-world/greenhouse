# SPDX-FileCopyrightText: 2023 peepo.world developers
#
# SPDX-License-Identifier: EUPL-1.2

import math
import multiprocessing

_max_threads = multiprocessing.cpu_count() * 2

worker_class = 'uvicorn.workers.UvicornWorker'
workers = min(1, math.floor(_max_threads / 8))
threads = min(1, math.ceil(_max_threads / workers))
