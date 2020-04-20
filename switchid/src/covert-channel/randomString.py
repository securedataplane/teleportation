#!/usr/bin/env python
#Author: Robert Kroesche
#Email: rkroesche@sec.t-labs.tu-berlin.de

import random, string


def random_string(length):
   random.seed(500)
   characters = string.ascii_letters + string.digits
   return ''.join(random.choice(characters) for i in range(length))