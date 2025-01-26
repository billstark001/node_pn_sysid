function init_guilda(env_vars)

    oldFolder = cd(env_vars.GUILDA_PRJ_PATH);
    matlab.project.loadProject(env_vars.GUILDA_PRJ_PATH);
    cd(oldFolder);

end