BASE = {
    "commands": {
        "startproject": {
            "app": [
                "__init__.py",
            ],
            "app > config": [
                "__init__.py",
                "config.py",
                "local_config.py.dist",
            ],
            "app > modules": [
                "__init__.py",
            ],
            "app > static": [],
        },

        "addmodule": {
            "app > modules > {{APP-NAME}}": [
                "__init__.py",
                "{{APP-NAME}}.py",
                "models.py",
                "views.py",
                "controllers.py",
            ]
        },
    },

    "replacement": {
        "{{APP-NAME}}": "**1"
    }
}
