BASE = {
    "commands": {
        "init": {
            "src": [
                "__init__.py",
            ],
            "src > config": [
                "__init__.py",
                "config.py",
                "local_config.py.dist",
            ],
            "src > modules": [
                "__init__.py",
            ],
            "src > static": [],
        },

        "startapp": {
            "src > modules > {{APP-NAME}}": [
                "__init__.py",
                "{{APP-NAME}}.py",
            ]
        },
    },

    "replacement": {
        "{{APP-NAME}}": "**1"
    }
}
