# Continuous Performance Evaluation for Signal/Collect


### Goal
The goal of this project is to provide a simple and easy to use script that automatically checks out the most recent version of the [Signal/Collect](https://github.com/uzh/signal-collect) project.

### Setup
* Place the continuousPerformanceEval folder in your home directory. (The folder could theoretically also be placed in another position but the managing all relative dependencies is up to you..)
* Put the absolute path to your continuousPerformanceEval for the baseDir field in the performanceEval.py file

### Running it
From within the continuousPerformanceEval directory run the following command:

```python performanceEval.py YOUR_GOOGLE_USERNAME YOUR_GOOGLE_PASSWORD```

If you want to force the script to run the evaluation even without the presence of new commits use:

```python performanceEval.py YOUR_GOOGLE_USERNAME YOUR_GOOGLE_PASSWORD debug```