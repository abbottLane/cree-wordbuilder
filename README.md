# cree-wordbuilder

Demo app to support the Plains Cree morph autocomplete FST models.

## Prereqs

1. Drop the weighted autocomplete model in the `language-service/backend/app/morphology/` directory. For example: `language-service/backend/app/morphology/crk-infl-morpheme-completion.weighted.hfstol`

2. Make sure the path to the `.hfstol` file is correct at the top of '`language-service/backend/app/morphology/fst.py`

3. Make sure you have `npm` version 6.14.4 or higher installed.

4. Make sure you have `python` version 3.6.5 or higher installed.

6. Make sure you have the `hfst` system binaries installed and properly configures to be found on your PATH 

## Run the client and server

1. Open a terminal window and start the client by navigating to the project root and typing `make run`. This will install a bunch of node dependencies and start the client.

2. Open a second terminal window, and `cd language-service/backend`. Type `make run` to start the language server. 

3. Point your browser at `http://localhost:3333/` to interact with the Cree wordbuilder.
