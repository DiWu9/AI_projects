# CSC320 class projects
Hello, I'm Woody. Welcome to my project description page for artificial intelligence class. Currently, I've finished two projects, and this page will keep updating for new projects.
Projects I have worked on since **Mar 15, 2020**:
1. **Chatbot**
2. **Missionaries and Cannibals**
3. **A* and the 8-puzzle**
4. **Konane Competition**
5. **Genetic Algorithms**
6. **Q-Learning Algorithms**
7. **Neural Networks: Back-Propagation**

For each project, I will briefly describe the goal of the project as well as some important implementations.

## Project 1: Chatbot [(Revised)](http://localhost:8888/edit/project-1-eliza/wups1.py)
A chatbot that can initialize a conversation with the user in English. The goal of the project is to enable the chatbot to speak like a human.

1. [Project](http://localhost:8888/tree/project-1-eliza)
2. [Revised Project](http://localhost:8888/notebooks/project-1-eliza/Revision_demo.ipynb)
3. [Independent Work](http://localhost:8888/notebooks/project-1-eliza/proj1-indep.ipynb)

### Functions
- **showKnowledge(self, inString)**:
The chatbot can tell some knowledge that is not commonly known.

- **tellJokes(self, inString)**:
The chatbot can tell jokes by first asking "Do you want to hear a joke?"

- **referPriorInputs(self, inString)**:
The chatbot can remember previous conversation and bring the old topic to conversation.

- **askName(self, inString)**:
The chatbot can ask user's name and remember the name when being asked.

- **askGender(self, inString)**:
The chatbot can ask user's gender and remember the gender when being asked.

- **askBirthday(self, inString)**:
The chatbot can ask user's birthday and remember the birthday when being asked.

- **introduceMyself(self, inString)**:
The chatbot can answer user's questions when being asked about name, birthday, or gender.

- **answerUserInfo(self, inString)**:
When user has told chatbot about his gender, birthday, and name. The chatbot can answer those information when user asks him again.

### Things achieved

- Tell jokes, knowledge
- Restate Sentence
- Remember name, birthday, and gender
- Able to answer its own name, birthday, and gender

### Things Iimporved in revision

- The chat agent will not ask the question that has already been asked.
- The chat agent will not repeat any jokes or knowledges, and it will not tell jokes or knowledge when there are no untold jokes in the memory.

### Things can be improved

- The chat agent is not good at retrieve keywords from a response. (For example, the chat agent cannot retrieve the word "male" from the sentence "I am a male").

## Project 2: Missionaries and Cannibals
Use BFS to solve the [Missionaries and Cannibals puzzle](https://www.youtube.com/watch?v=W9NEWxabGmg): to use a boat that can take at most 2 people to send 3 missionaries and 3 cannibals from one side of river to the other side.
The rule of Missionaries and Cannibals for this project is that missionaries on each side cannot outnumber cannibals (or cannibals on the side will be converted to missionaries).
There are two important files for the project:
- **missionary.py**: build the structure of the puzzle (tree)
- **search.py**: based on the tree build by missionary.py, find if the shortest path exists between the initial state and the goal state (an improved version is **improvedSearch.py**, which is more space-efficient by only expanding states that are not visited).

### Representation of states
The MissionaryState includes three instances:
- **start**: a string that represents the number of missionaries and cannibals on the start side. (e.g. "3M3C" represents the start side has 3 missionaries and 3 cannibals)
- **end**: a string that represents the number of missionaries and cannibals on the destination side.
- **operator**: a string that indicates the action just operated (e.g. sendTwoM: send two missionaries to destination)

The initial state prints like: **3M3C,0M0C**, and the goal state prints like **0M0C,3M3C**

1. [Project](http://localhost:8888/tree/project-2-cannibals)
3. [Independent Work](http://localhost:8888/notebooks/project-2-cannibals/proj2-indep.ipynb)

### Operator functions
- **sendTwoM()**
- **sendTwoC()**
- **sendMC()**
- **sendM()**
- **sendC()**
- **bringTwoM()**
- **bringTwoC()**
- **bringMC()**
- **bringM()**
- **bringC()**

The **send** operation means send people (person) to the destination, and **bring** means bring people back to start side. **send** and **bring** are called alternatively.

### Things Achieved

- Formulate the missionaries and cannibals problem to problem states and actions (for transitions).
- Apply state space search that begins on missionaries and cannibals initial state and searches for the final state.
- Improve search efficiency of state space search by only adding the states that have not been visited to the queue.

## Project 3: A* and the 8-puzzle
Apply **A*** search to the eight puzzle problem. The eight puzzle consists of a three be three board with eight numbered tiles and a blank space. A tile adjacent to he blank space can slide into the space. The object is to figure out the steps needed to get from one configuration of the tiles to another.

1. [Project](http://localhost:8888/tree/project-3-astar)
2. [Independent Work](http://localhost:8888/notebooks/project-3-astar/proj3-indep.ipynb)

### Things Achieved

- Implement informed search that can solve eight puzzle.
- Implement various heuristics (tiles out of place, Manhattan distance).
- Implement a representation of the [eight puzzle](https://www.geeksforgeeks.org/8-puzzle-problem-using-branch-and-bound/) state.

### Things Learned

- Trained to implement A* on multiple environments
- Practiced to write useful tests

## Project 4: Konane Competition
Implement the **minimax adversarial search** algorithm with **alpha-beta pruning** on the game of [Konane](https://youtu.be/09AAT29uaGE?t=28), also known as Hawaiian checkers.

- [Project](http://localhost:8888/tree/project-4-konane)

### Things Achieved

- Implement alpha-beta minimax adversarial search.
- Design and implement an efficient static evaluator considering its efficiency, relation to actual chances of winning, and the order of end states.
- Tests minimaxPlayer's performance under different searching depths.

### Things Can be Improved

- If time is allowed, the static evaluation can be improved considering its mediocre winning rate during the tournaments.
- If time is allowed, implement the minimax adversarial seach on other adversarial games.

## Project 5: Genetic Algorithms [(Revised)](http://localhost:8888/notebooks/project-5-ga/ga_analysis.ipynb)
Try to replicate Melanie Mitchell's [Royal Roads paper](https://melaniemitchell.me/PapersContent/ecal92.pdf), which is to evolve bitstrings using her two different RR measures in order to assign fitness.

1. [Project](http://localhost:8888/tree/project-5-ga)
2. [Revised Project](http://localhost:8888/notebooks/project-5-ga/ga_analysis.ipynb)


### Things Achieved

- Replicated RR GA, RR GA without intermediate, and HillClimber experiments from Melanie Mitchell's Royal Road paper.
- For each HillClimber, RR GA, and RR GA without intermediate levels, do 30 independent runs with different random seeds.
- For each experiments, aggregate the 30 data sets to display the minimum/maximum/mean fitness over 30 runs.
- Analyzed the result and compared it to the result described in Mitchell's Royal Roads paper.

### Things Imporved in Revision

- Clean up redundant code by directly importing classes
- In result, add graphs with analysis

### Things Can be Improved

- Implement and test two-point crossover's impact on the results.
- Try more fitness functions and test their impacts on the results.

## Project 6: Q-Learning Algorithms [(Revised)](http://localhost:8888/notebooks/project-6-q/Analysis%20(Revised).ipynb)

Implement Q-Learning in challenging environments.

1. [Project](http://localhost:8888/tree/project-6-q)
2. [Revised Project](http://localhost:8888/notebooks/project-6-q/Analysis%20(Revised).ipynb)
3. [Independent Work (Not Implemented)](http://localhost:8888/notebooks/project-6-q/proj6-indep.ipynb)

### Key Functions

- **learn**: perform q-learning within the given environment.
- **behave**: choose the actions from start state to finish state that maximize reward.

### Things Achieved

- Implement Q-Learning Agent with properties learning rate, discount rate, exploration rate, max steps, and max episodes.
- Enable Q-Learning Agent to learn and behave on CoffeeGame, FrozenLake-V0 environment, and Taxi-V3 environment.
- Gather data on agent's reward rate (average reward per 1000 episodes) over time.
- Try a wide range of learning rate, discount rate, and exploration rate to find the set of values that works the best.

### Things Imporved in Revision

- Add anlysis regarding to which combination of learning rate, discount rate, and exploration rate works best in each environment.
- Add comments on agent's increasing average reward.

## Project 7: Neural Networks: Back-Propagation
Implement back-propagation algorithm to train the program to solve **XOR problem** and **auto-association**.

- [Project](http://localhost:8888/tree/project-7-backprop)

### Things Achieved

- Forward Propagation Activation
- Train the network by backward propagating error
- Compute and output error for each training

### Analysis

- The back propagation algorithm is hard to debug because complicated math model is involved, which makes it hard to compute the expected output and compare it with the acutal value for each variable.
- For each Forward Propagation and Backward Propagation, loops are exucuted in order to compute the activation and error of each unit, which also contributes to the difficulity of debugging.

### Things can be Improved

- While doing this project, a great amount of time is killed by the process of debugging. If I can redo the project, I will write the pseudocode first and then start coding becasuse doing so can avoid most of the math error or unclear logic.
- The current version is only tested on the networks within 3 layers. If time is allowed, networks with more than 3 layers can be tested.
