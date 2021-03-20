## Running the project

This software runs only on windows due to windows.h library.

You can run by directly executing dining_philosophers.exe, but if you wish to change the log type or any timers, please check main.cpp and recompile.

To compile the project, use c++11. This project was originally compiled using g++ on windows with the following arguments: ```g++ main.cpp implementations/*.cpp -o dining_philosophers -std=c++11```

## How it works:

This is a simulation for the dining philosophers problem, in which each philosopher may be in one of the following states:

1. **Thinking**: In this state the philosopher doesn't hold any forks and just spend time waiting;
2. **Hungry**: After finish thinking the philosopher gets hungry and try to get a fork to his left or right (one at a time). He will never return a fork to the table when in this state and is aways trying to get 2 forks at the same time;
3. **Eating**: When the philosopher is hungry and gets two forks, he starts eating. After finished, he returns the forks to the table one at a time;

## Logs:

There are 3 forms of log: NONE, SIMPLE and ILLUSTRATED.

1. **NONE:**

  This is the simplest log format, it only outputs a message when a deadlock occurs.

2. **SIMPLE:**

  In this mode you will only see the philosophers separated by id and the respective state (hungry, thinking or eating), followed by a timestamp as shown in the image below. In this format the logs are not set by a constant timer, instead the states are printed only when they change.

![SIMPLE](https://github.com/12pedro07/FEI-CS/blob/main/CC7261-SistemasDistribuidos/dining_philosophers/imgs/SIMPLE.png)

3. **ILLUSTRATED:**

  In this last mode, a small simulation is shown as bellow.
  
![ILLUSTRATED](https://github.com/12pedro07/FEI-CS/blob/main/CC7261-SistemasDistribuidos/dining_philosophers/imgs/ILLUSTRATED.png)

  In the image above you can se the following markers:
  
  1 - The state of the the philosopher;
  
  2 - The forks that the philosopher is holding (in the example, philosopher #02 is holding the right fork, but not the left one);
  
  3 - The forks at the table. In the marked example, philosopher #02 has no forks available at his right or at his left.

  In addition, the total number of forks at the table and a timestamp are also shown;
  
  
- *Disclaimer:* Due to asynchronous operations, the visual log may seem bugged if displayed to quickly, but it's only a visual effect, the number of forks at the simulation is always the same as the number of philosophers
