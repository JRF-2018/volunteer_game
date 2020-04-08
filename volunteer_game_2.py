#!/usr/bin/python3
__version__ = '0.0.1' # Time-stamp: <2020-03-01T20:05:47Z>
## Language: Japanese/UTF-8

"""A simple simulation about game theory for volunteers."""

##
## License:
##
##   Public Domain
##   (Since this small code is close to be mathematically trivial.)
##
## Author:
##
##   JRF
##   http://jrf.cocolog-nifty.com/software/
##   (The page is written in Japanese.)
##

import random
import numpy as np
import argparse

## デフォルトでは Q4 の設定。
## Q2 の設定にしたいときは次のように指定する。
##
## $ python volunteer_game_2.py --tax=0
##
## Q1 の設定にしたいときは次のように指定する。
##
## $ python volunteer_game_2.py --max-labor-per-volunteer=1.0 \
##     --basic-reward-per-worker=0.0 --tax=0
##
## Q5 の設定にしたいときは次のように指定する。
##
## $ python volunteer_game_2.py --max-labor-per-volunteer=1.0 \
##     --basic-reward-per-worker=0.0 --tax=0.5

def parse_args ():
    global ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--fluid-population", default=998, type=int)
    parser.add_argument("--fixed-workers", default=1, type=int)
    parser.add_argument("--fixed-volunteers", default=1, type=int)
    parser.add_argument("--tax", default=2/3, type=float)
    parser.add_argument("--init-fluid-workers", default=None, type=int)
    parser.add_argument("--max-labor-per-volunteer", default=2.0, type=float)
    parser.add_argument("--min-labor-per-volunteer", default=1.0, type=float)
    parser.add_argument("--contribution-per-volunteer", default=4.0, type=float)
    parser.add_argument("--basic-reward-per-worker", default=1.0, type=float)
    parser.add_argument("--max-reward-per-worker", default=10000.0, type=float)
    parser.add_argument("--distributable-reward-per-worker", default=1.0, type=float)
    parser.add_argument("--labor-per-worker", default=1.0, type=float)
    parser.add_argument("--achievement-per-worker", default=1.0, type=float)
    parser.add_argument("--achievement-per-volunteer", default=1.0, type=float)

    ARGS = parser.parse_args()


class Economy:
    def __init__ (self, fluid_workers=None):
        fw = fluid_workers
        if fluid_workers is None:
            fluid_workers = random.randint(0, ARGS.fluid_population)
        self.fluid_workers = fluid_workers
        self.search_width = ARGS.fluid_population

    def step (self):
        workers = self.fluid_workers + ARGS.fixed_workers
        volunteers = ARGS.fluid_population - self.fluid_workers \
            + ARGS.fixed_volunteers
        population = workers + volunteers
        print("workers:volunteers :", workers, ":", volunteers)

        if volunteers < population / 2:
            labor_per_volunteer = ARGS.max_labor_per_volunteer
        else:
            labor_per_volunteer = max(ARGS.max_labor_per_volunteer 
                                      * (population / 2) / volunteers,
                                      ARGS.min_labor_per_volunteer)

        gross_utility_by_volunteers = ARGS.contribution_per_volunteer \
            * np.clip(volunteers, 0, population / 2)

        reward_per_worker = ARGS.basic_reward_per_worker \
            + ARGS.distributable_reward_per_worker * (population / workers)
        reward_per_worker = min(reward_per_worker,
                                ARGS.max_reward_per_worker)
        tax_per_worker = reward_per_worker * ARGS.tax
        reward_per_volunteer = (tax_per_worker * workers) / volunteers

        utility_per_worker = reward_per_worker - tax_per_worker \
            - ARGS.labor_per_worker + ARGS.achievement_per_worker \
            + (gross_utility_by_volunteers / population)

        utility_per_volunteer = reward_per_volunteer \
            - labor_per_volunteer + ARGS.achievement_per_volunteer \
            + (gross_utility_by_volunteers / population)

        print("utility of workers:volunteers :",
              utility_per_worker, ":", utility_per_volunteer)
        print("gross utility :", utility_per_volunteer * volunteers
              + utility_per_worker * workers)

        ## 効用が大きい方の比率を増やしながら、ほぼ utility_per_worker
        ## == utility_per_volunteer となる解を二分探索する。
        fw = self.fluid_workers
        sw = np.ceil(self.search_width / 2)
        if utility_per_worker == utility_per_volunteer:
            pass
        elif utility_per_worker > utility_per_volunteer:
            if (ARGS.fluid_population - fw) / 2 < sw:
                sw = np.ceil((ARGS.fluid_population - fw) / 2)
            fw += sw
        else:
            if fw / 2 < sw:
                sw = np.ceil(fw / 2)
            fw -= sw
        fw = np.clip(fw, 0, ARGS.fluid_population)
        self.fluid_workers = fw
        self.search_width = sw


def run ():
    economy = Economy(fluid_workers=ARGS.init_fluid_workers)
    prev_fw = economy.fluid_workers
    prev_fw2 = -1
    step = 1
    while True:
        print("\nStep", step)
        economy.step()
        ## workers:volunteers の比率が以前と同じか、単純な振動解になっ
        ## たとき終了。
        if prev_fw == economy.fluid_workers:
            break
        if prev_fw2 == economy.fluid_workers:
            break
        prev_fw2 = prev_fw
        prev_fw = economy.fluid_workers
        step += 1


if __name__ == '__main__':
    parse_args()
    run()
