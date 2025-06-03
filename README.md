# Scope

Sample project to understand vectorization of texts and learn python 

- plan to use different models for vectorization to see what works.
- understand if possible what additional context has to be stored along with the vector embeddings in postgres for effective retirieval, can we be basically do some sort of knowledge security restriction based on access levels in a org

# Dev Considerations & Info

using the below to make sure the models are not cached in default location on windows - default is user home location with .cache dir, earlier was `TRANSFORMERS_CACHE` which is deprecated now

`export HF_HOME=[home  location]`

- uv is the tool used for package managment
- yoyo migrations for db migrations0 
    - use `yoyo [command] -p` to make sure it prompts for password 
    - use `-b` -- batch mode to get rid of user prompts when doing things. `yoyo list`, `yoyo apply`