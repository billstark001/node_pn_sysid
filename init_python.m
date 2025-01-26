function init_python(env_vars)
    
    pythonPath = '/opt/anaconda3/bin/python';
    
    if isfield(env_vars, 'CONDA_PYTHON_EXE')
        pythonPath = env_vars.CONDA_PYTHON_EXE;
    elseif isfield(env_vars, 'PYTHON_PATH')
        pythonPath = env_vars.PYTHON_PATH;
    elseif isfield(env_vars, 'PYTHON_EXE')
        pythonPath = env_vars.PYTHON_EXE;
    end
    
    pyenv(Version = pythonPath);
    pyenv(ExecutionMode = "OutOfProcess");

end