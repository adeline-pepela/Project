@echo off
echo Installing Graphviz using pip...
pip install graphviz

echo.
echo Downloading Graphviz Windows installer...
curl -L -o graphviz-installer.exe https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/8.1.0/windows_10_cmake_Release_graphviz-install-8.1.0-win64.exe

echo.
echo Running Graphviz installer...
echo Please follow the installation instructions and make sure to check "Add Graphviz to the system PATH"
graphviz-installer.exe

echo.
echo After installation completes, please restart your Jupyter notebook or Python environment.
pause