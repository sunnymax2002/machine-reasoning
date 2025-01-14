# Setup TypeDB

1. Install Java, then set JAVA_HOME as well as add %JAVA_HOME%\bin to path
2. Run typedb server using admin command prompt - windows terminal or powershell won't work

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