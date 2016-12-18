import numpy as np
import copy

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.visited = [[0,0]] #A list of the places visited already by the robot
        #self.tolerate = 0 #for tolerating getting stuck once and after that get back to previous point
    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        #Creating the list of candidates that can be visited from the robot's place
        

        print "The location of robot is ... ", self.location
        #print "The sensors values are: for left, ", sensors[0], "for center: ", sensors[1], " and for right: ", sensors[2] 
        
        self.visited.append (copy.copy(self.location))
        #print "self.visited is : \n"
        #for i in range (len (self.visited)):
         #   print self.visited[i]


        list_candidates = self.generateCandidates(sensors)
        
        #Omitting the visited places from the candidates list
        i = 0
        j = len (list_candidates)
        while i < j: 
        #for i in range (len(list_candidates) - 1, 0, -1):
            if list_candidates[i] in self.visited:
                list_candidates.pop(i)
                j -= 1
            else:
                i += 1

        #omit all the possible states with distance more than one
        list_candidates = self.findCandidateDistanceOne(list_candidates)

        print "The candidates are... \n"
        for i in range (len(list_candidates)):
            print list_candidates[i]
        # Finding best candidate, closest to goal, from the remaining candidates
        
        if len(list_candidates) == 0:

            index = self.visited.index(self.location)
            rotation = 0
            print "The latest visit was: ", self.visited[index - 1]

            if self.visited[index - 1][0] < self.location[0]:
                if self.heading == 'up':
                    rotation = 90
                    movement = 0
                    self.heading = 'right'
                elif self.heading == 'right':
                    rotation = 90
                    movement = -1 * (self.visited[index - 1][0] - self.location[0])
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'down'
                elif self.heading == 'left':
                    rotation = -90
                    movement = -1 * (self.visited[index - 1][0] - self.location[0])
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'down'
                else:
                    rotation = 0
                    movement = -1 * (self.visited[index - 1][0] - self.location[0])
                    self.location = copy.copy(self.visited[index - 1])
            elif self.visited[index - 1][0] > self.location[0]:
                if self.heading == 'up':
                    rotation = 0
                    movement = -1 * (self.location[0] - self.visited[index - 1][0])
                    self.location = copy.copy(self.visited[index - 1])
                elif self.heading == 'right':
                    rotation = -90
                    movement = -1 * (self.location[0] - self.visited[index - 1][0])
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'up'
                elif self.heading == 'left':
                    rotation = 90
                    movement = -1 * (self.location[0] - self.visited[index - 1][0])
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'up'
                else:
                    rotation = 90
                    movement = 0
                    self.heading = 'left'

            elif self.visited[index - 1][1] > self.location[1]:
                if self.heading == 'up':
                    rotation = 90
                    movement = self.visited[index - 1][1] - self.location[1]
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'right'
                elif self.heading == 'right':
                    rotation = 0
                    movement = self.visited[index - 1][1] - self.location[1]
                    self.location = copy.copy(self.visited[index - 1])
                elif self.heading == 'down':
                    rotation = -90
                    movement = self.visited[index - 1][1] - self.location[1]
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'right'
                else:
                    rotation = 90
                    movement = 0
                    self.heading = 'up'
            else:
                if self.heading == 'up':
                    rotation = -90
                    movement = self.location[1] - self.visited[index - 1][1]
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'left'
                elif self.heading == 'left':
                    rotation = 0
                    movement = self.location[1] - self.visited[index - 1][1]
                    self.location = copy.copy(self.visited[index - 1])
                elif self.heading == 'down':
                    rotation = 90
                    movement = self.location[1] - self.visited[index - 1][1]
                    self.location = copy.copy(self.visited[index - 1])
                    self.heading = 'left'
                else:
                    rotation = 90
                    movement = 0
                    self.heading = 'down'
            
            
        else:
            
            best_candidate_distance = [list_candidates[0], self.distance_to_goal(list_candidates[0])]
            for i in range (1, len(list_candidates)):
                if self.distance_to_goal(list_candidates[i]) <= best_candidate_distance[1]:
                    best_candidate_distance = [list_candidates[i], self.distance_to_goal(list_candidates[i])]

            #Steering toward the chosen best point
            if best_candidate_distance[0][1] > self.location[1]: #best location has a bigger x value 
                movement = best_candidate_distance[0][1] - self.location[1]
                self.location[1]+= movement
                
                if self.heading == 'up': #Agent needs to move right
                    rotation = 90     
                elif self.heading == 'right': #Agent needs to move forward
                    rotation = 0
                elif self.heading == 'down':
                    rotation = -90
                else: # heading is left should never happen
                    print "impossible state entered"
                self.heading = 'right'    
            elif best_candidate_distance[0][1] < self.location[1]: #best location has a lower x value

                movement = self.location[1] - best_candidate_distance[0][1]
                self.location[1]-= movement
                
                if self.heading == 'up':
                    rotation = -90
                elif self.heading == 'left':
                    rotation = 0
                elif self.heading == 'down':
                    rotation = 90
                else: #heading is right and should never happen
                    print "impossible state entered"
                self.heading = 'left'
            elif best_candidate_distance [0][0] > self.location[0]: #Best location has a higher y value
                
                movement = best_candidate_distance[0][0] - self.location[0]
                self.location[0] += movement
                
                if self.heading == 'up':
                    rotation = 0
                elif self.heading == 'right':
                    rotation = -90
                elif self.heading == 'left':
                    rotation = 90
                else: #heading is downward and should never happen
                    print "impossible state entered"
                self.heading = 'up'
            else: #Best location has a lower y value

                movement = self.location[0] - best_candidate_distance[0][0]
                self.location[0] -= movement
                
                if self.heading == 'down':
                    rotation = 0
                elif self.heading == 'right':
                    rotation = 90
                elif self.heading == 'left':
                    rotation = -90
                else: #heading is upward and should never happen
                    print "impossible state entered"
                self.heading = 'down'
        print rotation, '   ,', movement, '  ,', self.heading
            #rotation = 0
        #movement = 0

        return rotation, movement 


    # Required helper functions written by Armin
    def generateCandidates (self, sensors):
        '''
        This function creates all the possible points that the robot can reach
        from it's current location as the candidates of the robot movement
        based on the sensor inputs the robot adds the required constatnts to the 
        current location to decide how many cubes it can move to the directions 
        it's allowed to move.
        '''
        list_of_candidates = []
        if sensors[2] == 0:
            pass
        elif sensors[2] < 3:
            for i in range (sensors[2] ):
                if self.heading == 'up':
                    list_of_candidates.append ([self.location[0], self.location[1] + i + 1])
                elif self.heading == 'right':
                    list_of_candidates.append ([self.location[0] - i - 1, self.location[1]])
                elif self.heading == 'left': 
                    list_of_candidates.append ([self.location[0] + i + 1, self.location[1]])
                else: #Heading is downward
                    list_of_candidates.append ([self.location[0] , self.location[1] - i - 1])

        else:
            for i in range (3):
                if self.heading == 'up':
                    list_of_candidates.append ([self.location[0], self.location[1] + i + 1])
                elif self.heading == 'right':
                    list_of_candidates.append ([self.location[0] - i - 1, self.location[1]])
                elif self.heading == 'left': 
                    list_of_candidates.append ([self.location[0] + i + 1, self.location[1]])
                else: #Heading is downward
                    list_of_candidates.append ([self.location[0] , self.location[1] - i - 1])
        if sensors[1] == 0:
            pass
        elif sensors[1] < 3:
            for i in range (sensors[1] ):
                if self.heading == 'up':
                    list_of_candidates.append ([self.location[0] + i + 1, self.location[1]])
                elif self.heading == 'right':
                    list_of_candidates.append ([self.location[0] , self.location[1]+ i + 1] )
                elif self.heading == 'left':
                    list_of_candidates.append ([self.location[0] , self.location[1] - i - 1])
                else: #Heading is downward
                    list_of_candidates.append ([self.location[0] - i - 1, self.location[1]])
        else:
            for i in range (3):
                if self.heading == 'up':
                    list_of_candidates.append ([self.location[0] + i + 1, self.location[1]])
                elif self.heading == 'right':
                    list_of_candidates.append ([self.location[0] , self.location[1]+ i + 1] )
                elif self.heading == 'left':
                    list_of_candidates.append ([self.location[0] , self.location[1] - i - 1])
                else: #Heading is downward
                    list_of_candidates.append ([self.location[0] - i - 1, self.location[1]])
        if sensors[0] == 0:
            pass
        elif sensors[0] < 3:
            for i in range (sensors[0] ):
                if self.heading == 'up':
                   list_of_candidates.append ([self.location[0] , self.location[1]- i - 1] )
                elif self.heading == 'right':
                    list_of_candidates.append ([self.location[0] + i + 1, self.location[1]] )
                elif self.heading == 'left':
                    list_of_candidates.append ([self.location[0] - i - 1, self.location[1]] )
                else: #Heading is downward
                    list_of_candidates.append ([self.location[0] , self.location[1] + i + 1] )
        else:
            for i in range (3):
                if self.heading == 'up':
                    list_of_candidates.append ([self.location[0] , self.location[1]- i - 1] )
                elif self.heading == 'right':
                    list_of_candidates.append ([self.location[0] + i + 1, self.location[1]] )
                elif self.heading == 'left':
                    list_of_candidates.append ([self.location[0] - i - 1, self.location[1]] )
                else: #Heading is downward
                    list_of_candidates.append ([self.location[0] , self.location[1]+ i + 1 ] )
        return list_of_candidates

    def distance_to_goal (self, location):
        '''
        This function gets as input an arbitrary ocation and calculates
        the distance from this point to the goal
        The goal to distenation is defined as the average distance of the
        point to the 4 goal points hence we calculate the distance of all the
        goal points to the arbitrary point and divide it by 4 when returning
        '''
        dim = self.maze_dim
        #Creating the 4 goal locations of the maze based on the maze dimension
        goal_locations = [[dim / 2, dim / 2], [dim / 2 - 1, dim / 2],
                          [dim / 2, dim / 2 - 1], [dim / 2 - 1, dim / 2 - 1]]
        distance = 0
        for i in range (4):
            distance += abs (location[0] - goal_locations[i][0]) + abs (location[1] - goal_locations[i][1])
        return distance / 4.0

    def findCandidateDistanceOne (self, list_of_candidates):
        '''
        This function gets the list of possible candidates and only selects the ones with distance one to the 
        robot's current location
        '''
        possible_candidates = []
        for elements in list_of_candidates:
            if abs(elements[0] - self.location[0]) + abs (elements[1] - self.location[1]) == 1:
                possible_candidates.append (elements)

        return possible_candidates

    def reachedGoal (self):
        '''
        This function is a boolean functions that returns true when the agent has reached the goal in the maze
        '''  
        dim = self.maze_dim
        #Creating the 4 goal locations of the maze based on the maze dimension
        goal_locations = [[dim / 2, dim / 2], [dim / 2 - 1, dim / 2],
                          [dim / 2, dim / 2 - 1], [dim / 2 - 1, dim / 2 - 1]]

        return self.location in goal_locations