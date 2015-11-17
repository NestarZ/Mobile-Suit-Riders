from django.db import models

import sys
sys.path.insert(0, '/home/nestarz/Github/Mobile-Suit-Riders/src')

import instances

# Create your models here.
class Grid(models.Model):
    line_size = models.BigIntegerField()
    column_size = models.BigIntegerField()
    obstacle_amount = models.BigIntegerField()
    pub_date = models.DateTimeField('date published')
    grid = ""
    robot_pos = ""

    def generate(self):
        self.grid = instances.generate_grid(int(self.line_size),
                                            int(self.column_size),
                                            int(self.obstacle_amount))
        self.robot_pos, self.goal, self.robot_ori = instances.generate_robot(self.grid)
        self.save()
