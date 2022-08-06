## Scala Native Incremental Compilation Autotest


### Requirement
Linux environment, sbt, python3. 

I test the script in wsl Ubuntu, sbt 1.6.1 and python 3.8. The package `regex` and `pandas` are required. In the python script, I use `regex` instead of `re` to do the pattern matching, since `re` doesn't support the variable width of lookahead regex. 
### Usage

Run the command

```
./autotest --scala SCALA-VERSION --scala-native SCALA-NATIVE-VERSION --benchmark-list <benchmarks list or non to run all>
```

Or use the default configuration

```
./autotest
```

### Explanation 
The script automatically test the correctness and performance of incremental compilation in Scala Native. After running this script, the performance is presented in the file `result`. There are some keywords in this file:

* __WARMUP PHASE__: the phase is used for warmming up sbt. Just ignore it.

* __COMPILE PHASE__: After cleaning the `target`, this phase compiles the scala project from scratch. 

* __EDIT PHASE__: We modify some source codes of scala project and then recompile it. In this phase, only very little source code is changed. 

* __TRANSITION PHASE__: We directly change the source code from one main class to another main class. Therefore many libraries changes and source code changes are applied. Since too many changes are applied, the advantages of incremental compilation are suppressed. Therefore, we only use it to test the correctness of incremental compilation. 

## Result

The result is presented in the `comparison` directory.