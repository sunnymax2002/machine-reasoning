# Setup TypeDB for Windows

Install the following

1. [JDK for Windows]()

2. [TypeDB Server]() - local server for development, and later this can be replaced by cloud server

3. [TypeDB Studio]() - this is good to experiment and visualize graph data, but console is better for scripting and automation

4. [TypeDB Console]() - TODO: seems console is installed alongwith server

## Running the tools

1. Install Java, then set JAVA_HOME as well as add %JAVA_HOME%\bin to path
2. Run typedb server/console using admin command prompt - windows terminal or powershell won't work

# Python Driver

## WSL Ubuntu

```console
# Setup Python Virtual Environment

cd $GIT_REPOS/machine-reasoning/basics/graph_db/typedb_v2
virtualenv .vnv
```
## Windows

```console
chdir %GIT_REPOS%\machine-reasoning\basics\graph_db\typedb_v2

python -m venv .venv
```