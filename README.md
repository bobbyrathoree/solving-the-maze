# Assignment 0
## Part 1

In the first part of the assignment, we're given a skeleton code that starts out by assuming the fringe to be a stack, which is not the way to go for a search algorithm in this case. Whenever a node is visited, it should be FIFO-d, which means its neighboring nodes should be explored first. In the given skeleton code however, when a new node is added to the fringe, it is explored right away, instead of the older (parent) one.

I could've used a priority queue for this problem since it is similar to Dijkstra's algorithm, but decided to with a regular queue with a little twist. Along with the coordinates of the node that is to be explored next, I coupled it with the path it took to get there as a tuple, which takes care of "backtracking" automatically.

I altered the default moves that are fixed throughout the scope of the problem: added directions (N,S,E,W) to each of them as part of a tuple. This helps us in keeping track of visited states. Speaking of which, changing a stack to a queue pretty much solved the problem (outputs the correct distance travelled till Luddy Hall). But it is not optimized, since it goes through the visited states multiple times, hence increasing overhead. To prevent it from doing that and to solve the problem in literally 1/10th the time, I added a list to keep track of the nodes that have been visited. So, now when we talk about valid moves, it also includes not being in the visited state. visited is a **set** instance to only add to it **unique** nodes coordinates.

Whenever a solution is not found, it had to return None. To implement that, I took some time to come up with a solution that didn't involve a lot of backtracking. I figured that if all the sidewalks are visited, there is no point in continuing further. So to return None whenever a solution doesn't exist, I compared the length of visited set and the number of sidewalks in the graph (that are fixed no matter what). If they're equal, we arrive at our conclusion.

