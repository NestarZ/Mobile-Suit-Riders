from django.db import models

import sys
sys.path.insert(0, '/home/nestarz/Github/Mobile-Suit-Riders/src')

import instances
import main

# Create your models here.
class Grid(models.Model):
    line_size = models.BigIntegerField()
    column_size = models.BigIntegerField()
    obstacle_amount = models.BigIntegerField()
    pub_date = models.DateTimeField('date published')
    grid = []
    robot_pos = []
    path = []

    def generate(self):
        self.grid = instances.generate_grid(int(self.line_size),
                                            int(self.column_size),
                                            int(self.obstacle_amount))
        self.robot_pos, self.goal, self.robot_ori = instances.generate_robot(self.grid)

    def solve(self):
        graph = main.generateGraph(self.grid)
        self.path = graph.bfs_paths((self.robot_pos, self.robot_ori), self.goal)
        self.path_cases = list(set([x[0] for x in self.path]))
