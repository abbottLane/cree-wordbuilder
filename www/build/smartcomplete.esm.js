import { p as patchBrowser, g as globals, b as bootstrapLazy } from './core-6a64acb2.js';

patchBrowser().then(options => {
  globals();
  return bootstrapLazy([["smart-complete",[[1,"smart-complete",{"backend":[1],"throttle":[2],"limit":[2],"searchresults":[32],"dictionaryresults":[32],"status":[32]}]]]], options);
});
