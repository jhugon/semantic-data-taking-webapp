# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v1.5.3](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.5.3) - 2023-03-22

- [`639dd7d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/639dd7dd130ecc1b3258bed1f7f7914782a3f2b9) fix: bump Jena-Fuseki Dockerfile versions
- [`35a41b6`](https://github.com/jhugon/semantic-data-taking-webapp/commit/35a41b643a6d01801d35057e8e57beee251c5fc2) docs: remove ` type from README.md
- [`bf4ac7b`](https://github.com/jhugon/semantic-data-taking-webapp/commit/bf4ac7b6f2d62cf7b4646d1851de25a2a7170d2b) chore: update pre-commit config versions

## [v1.5.2](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.5.2) - 2022-10-05

- [`441aedf`](https://github.com/jhugon/semantic-data-taking-webapp/commit/441aedf2242b531407cf03af7f8e8315d5cbe674) fix: data table view now shows "" instead of "None"

## [v1.5.1](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.5.1) - 2022-10-05

- [`026f7b4`](https://github.com/jhugon/semantic-data-taking-webapp/commit/026f7b4b06ccbfbb40fb72bcb98c2b352597c885) fix: remove debug info in enterdata page

## [v1.5.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.5.0) - 2022-10-03

- [`cbd348c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/cbd348cb199a9ea7765ef2a5c054ce2f4ba7582f) Merge pull request #47 from jhugon/geolocation
- [`71cbc84`](https://github.com/jhugon/semantic-data-taking-webapp/commit/71cbc845f5fb76bfb78ba1160a9c83d3573b3281) fix(db): commented out debug log level
- [`b3b8818`](https://github.com/jhugon/semantic-data-taking-webapp/commit/b3b8818aaf0a71f05bbeb4e34c453b48b5f22afd) feat(db): get data for geo points
- [`54fbc4c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/54fbc4caf8dc1613ae77258a46986bbfca00ecf7) feat(db): can now submit geo points to db
- [`8b891ad`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8b891ad55320c0e3afe8b2ed71ec3bdaf8f25d21) feat(enterdata): got geolocation forms working correctly
- [`6fa40e4`](https://github.com/jhugon/semantic-data-taking-webapp/commit/6fa40e4f4c5c55b1c4c06c78c9641f60b5a02098) feat: working on putting geoloc in form
- [`ff2464c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/ff2464c58f92003b12dab6cb61bb8e316486a7a1) feat: can now add a prop that is a geographic point
- [`12f0bc5`](https://github.com/jhugon/semantic-data-taking-webapp/commit/12f0bc541d876c90e1326e83559dc1cc1999b9fa) feat: added strawman geolocation test to enterdata page

## [v1.4.1](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.4.1) - 2022-10-03

- [`32dbb49`](https://github.com/jhugon/semantic-data-taking-webapp/commit/32dbb49d967d14c709c3607986ac477dfbdba01b) fix: made navbar responsive with drop down button

## [v1.4.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.4.0) - 2022-09-29

- [`e48397e`](https://github.com/jhugon/semantic-data-taking-webapp/commit/e48397e43efb3707e3311d816f43e21c449e52a3) Merge pull request #45 from jhugon/back_to_feature_menu
- [`a139787`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a139787e94916547e2d3072a6baf407b38bcbe95) feat: added "back to feature menu" nav button
- [`6923cfa`](https://github.com/jhugon/semantic-data-taking-webapp/commit/6923cfa2ceef16e9d98f93de1b3529e2c0e728e2) fix: added bandit to dev deps to make pre-commit work
- [`8af8548`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8af8548ea964818a030e15fe2ed8569c8529efa8) fix: add cryptography lib to dev deps

## [v1.3.1](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.3.1) - 2022-08-20

- [`c42c25e`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c42c25e9694ecb1a8c85f1b6083e453394655494) fix(uplift): added .uplift.yml to manage bumping ver

## [v1.3.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.3.0) - 2022-08-20

- [`58975a1`](https://github.com/jhugon/semantic-data-taking-webapp/commit/58975a1dc279d5cb08431c478c6747595fa6926e) feat: added version to navbar

## [v1.2.1](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.2.1) - 2022-08-20

- [`acae939`](https://github.com/jhugon/semantic-data-taking-webapp/commit/acae939cbb9a62a44997070061294133a6c3c917) fix: fix DB getData bug introduced in c62e662dcf
- [`e78cc9c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/e78cc9c621f1764dc3db585a28aacebb2fa78ea8) chore: got rid of uneccesary logging class in db.py

## [v1.2.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.2.0) - 2022-08-20

- [`8cd88cc`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8cd88cca600f709306a3924ccc935b13a9c790a9) Merge pull request #43 from jhugon/speed-up-adddata
- [`c62e662`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c62e662dcf4fcc3853b5add0666924efd9159608) perf: submit data now done with a single DB transaction
- [`3cf8a35`](https://github.com/jhugon/semantic-data-taking-webapp/commit/3cf8a350169b85984fb7c487fa206aaf736359da) feat: add cmd line option to web.py for profiling

## [v1.1.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.1.0) - 2022-08-18

- [`c6bd973`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c6bd97339c134a261cbcb91132520aab6f5ac57f) feat: Add button to download all RDF data
- [`2aa7a6e`](https://github.com/jhugon/semantic-data-taking-webapp/commit/2aa7a6edce4fd26e6cdeebb41ea437816915556f) feat: Added download CSV to feature page
- [`89e702c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/89e702c892f427a124ef06eb50c2b60d94eb3822) build: put gunicorn in Pipfile

## [v1.0.1](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.0.1) - 2022-08-16

- [`882d836`](https://github.com/jhugon/semantic-data-taking-webapp/commit/882d8365e762ee3f7ddd6c39824b3421b73e5774) fix(docker): only bind directories, not files

## [v1.0.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v1.0.0) - 2022-08-13

- [`392a74c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/392a74ce63c8dab6c6ffeee21d2a330bfa918a9c) Merge pull request #39 from jhugon/category_properties
- [`a3f6861`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a3f6861a6b249ce2de084b01c63c19d35d6fe613) feat: table view categories working now
- [`8e6c7cf`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8e6c7cfff6cb0cd73573183894c25439ecb984fa) feat: categories work in data entry
- [`8cd057d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8cd057d2605f6c89b489b6a413aaccd24bc4d36b) feat: now categorical shows up on feature page
- [`f1cb542`](https://github.com/jhugon/semantic-data-taking-webapp/commit/f1cb542b64e21610e0b0f8bb95e181ace30bc52b) feat!: can now add categorical properties

## [v0.4.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v0.4.0) - 2022-08-11

- [`c9024ce`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c9024ce998ec1f6263e7b3a31641260f1350b5ab) feat: add login session persistance

## [v0.3.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v0.3.0) - 2022-08-09

- [`c2fac84`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c2fac8479d91cc4bb354dc8ce975c33e6fde7a1c) Merge pull request #34 from jhugon/improve_comments
- [`496f009`](https://github.com/jhugon/semantic-data-taking-webapp/commit/496f009244300958cb5d0cc038d48a8c6bf21416) feat: data table now shows comments (from stimuli)
- [`5a59ac0`](https://github.com/jhugon/semantic-data-taking-webapp/commit/5a59ac0ff0bbccfe607117dacac3a198f39c920e) fix: only comment on stimuli, not observations
- [`f7a3e94`](https://github.com/jhugon/semantic-data-taking-webapp/commit/f7a3e94961999ba6b82540addc786f0e0dc79367) feat: added comment field for data entry
- [`b8467e8`](https://github.com/jhugon/semantic-data-taking-webapp/commit/b8467e8d7a74977755fc2969de9f671cf331feee) fix: property comments show up now
- [`e165f59`](https://github.com/jhugon/semantic-data-taking-webapp/commit/e165f591e7ed60a942b78bebb089910305ca6895) feat: Add comments and properties to feature page

## [v0.2.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v0.2.0) - 2022-08-09

- [`0e7eced`](https://github.com/jhugon/semantic-data-taking-webapp/commit/0e7eced0ef35293b3d26e301874c86faea27d9ff) feat: Dockerfile just install pkgs from Pipfile.lock
- [`217f4d1`](https://github.com/jhugon/semantic-data-taking-webapp/commit/217f4d109c0b92a48159e68e9a20866bbd0ec66a) fix: add back berkeleydb package (broke w/ last commit)

## [v0.1.1](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v0.1.1) - 2022-08-09

- [`ab18a31`](https://github.com/jhugon/semantic-data-taking-webapp/commit/ab18a313728bb94bd569689db5ee131feb3a50e1) chore(DB): BerkeleyDB backend doesnt work anymore so clean up
- [`876b884`](https://github.com/jhugon/semantic-data-taking-webapp/commit/876b8847a04a6676533039e9aa12c7190428bdf3) fix: made DB code more resilient to coming up before DB
- [`722e78c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/722e78c6967c644e304ec7f32248d45c05b6ae7a) ci: adding black.yml CI workflow
- [`73c9cd5`](https://github.com/jhugon/semantic-data-taking-webapp/commit/73c9cd5caf8da53aef3e6e1bb83de3802615f908) ci: moved uplift workflow to uplift.yml
- [`86a3ae3`](https://github.com/jhugon/semantic-data-taking-webapp/commit/86a3ae336d1ee3af83c8d3dd07e86bc7430c0c0a) ci: installed and ran pre-commit plugins, inc. black

## [v0.1.0](https://github.com/jhugon/semantic-data-taking-webapp/releases/tag/v0.1.0) - 2022-08-09

- [`7fae9d9`](https://github.com/jhugon/semantic-data-taking-webapp/commit/7fae9d9c79405d6cde15b6078287a5d53cd37a1b) ci: added Uplift CI for conventional commits
- [`7da5375`](https://github.com/jhugon/semantic-data-taking-webapp/commit/7da537578363bacc913a650b6f8808d889e62a17) chore: Merge pull request #30 from jhugon/SSL
- [`abb3e75`](https://github.com/jhugon/semantic-data-taking-webapp/commit/abb3e750d370fea491a2fa9281dcd193d22ba19b) fix: flask-simple-login update--dont print passwords
- [`29ea863`](https://github.com/jhugon/semantic-data-taking-webapp/commit/29ea86302b323028defd9619f958196e7aa2b9b3) feat(web): log that secret key is loaded from environment
- [`849db7f`](https://github.com/jhugon/semantic-data-taking-webapp/commit/849db7fea3a63bb719abed00cb0c751cfa46a5d1) feat(web): configured security headers to be extra secure
- [`57f47a4`](https://github.com/jhugon/semantic-data-taking-webapp/commit/57f47a45938b653314a2660c546fa575d7244318) feat(Nginx): server tokens all off
- [`6b7e472`](https://github.com/jhugon/semantic-data-taking-webapp/commit/6b7e4720bd2d8ed04c1b9eedabbd6accf6a45d9d) feat: Nginx container now usses TLSv1.3
- [`c497e4b`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c497e4b77d973eb698e1b0ffc9f93a2c673f860d) feat: Enable Flask-Talisman & SSL in test server
- [`2b2db3e`](https://github.com/jhugon/semantic-data-taking-webapp/commit/2b2db3e9a6cbc30d0927273b894696990b3c0542) feat(fuseki): docker compose log to GCP
- [`2281426`](https://github.com/jhugon/semantic-data-taking-webapp/commit/22814266012f6c1d6fb3f1016430ed5f49072089) chore: Merge pull request #28 from jhugon/cloudrun
- [`d715259`](https://github.com/jhugon/semantic-data-taking-webapp/commit/d7152598e3a36ce047e811e43efa181671ae224a) feat(docker): add jena-fuseki/docker-compose.yml
- [`72656f2`](https://github.com/jhugon/semantic-data-taking-webapp/commit/72656f247b0c71287f22cf45abe2cbc765f30216) refactor: delete Docker.cloudrun and make it a softlink
- [`0027d5f`](https://github.com/jhugon/semantic-data-taking-webapp/commit/0027d5fb663e576b075365ad979cd91bf49708ff) chore: Merge branch main into cloudrun
- [`294c329`](https://github.com/jhugon/semantic-data-taking-webapp/commit/294c32997e2eec6ff236a43523e7524d850d31c4) refactor(web.py): use factory pattorn with app
- [`1bebcd1`](https://github.com/jhugon/semantic-data-taking-webapp/commit/1bebcd1368974d69073e1a75472404988ab4970b) Merge branch main into cloudrun
- [`549ffe8`](https://github.com/jhugon/semantic-data-taking-webapp/commit/549ffe80028f508d458c2576a00a364bb783a217) Merge pull request #23 from jhugon/sparql_server
- [`fd151bd`](https://github.com/jhugon/semantic-data-taking-webapp/commit/fd151bd26487b2fa8c5722d49d40ca17a920d04e) Got app connecting to sparql store in Docker
- [`46bad5d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/46bad5d308914bf2cc74b5ad862722a3ca5882da) use sparql query to build quantity kind list
- [`6a4c1f8`](https://github.com/jhugon/semantic-data-taking-webapp/commit/6a4c1f81b1d834d615104cd56c6aa0971985954c) more work on queries
- [`3f83b1b`](https://github.com/jhugon/semantic-data-taking-webapp/commit/3f83b1b7ca25a81b45cb5dc15cd5bac148bcb6b4) working on sparql queries
- [`a86c1fd`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a86c1fd7d974ef0060c6737d2834dcf278d942f5) use sparql graph store proto to upload vocabs
- [`319fe5d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/319fe5d9b174ba076ffdbe8df15eee87e80a262f) make my own quads and triples methods on DBInterface
- [`3c232a5`](https://github.com/jhugon/semantic-data-taking-webapp/commit/3c232a5b400a2c9d3e5a2c1f91213cc22b3f0aeb) messing with diff ways to get quads/triples to make work with jena
- [`a0b1aaa`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a0b1aaadf325edb06eef27b93040859efc494320) working on getting db to work with jena-fuseki
- [`a27e218`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a27e218d9b207d3a56e80e1d6469491653268f15) fix bug introduce that messes up unit sybols in tables
- [`b15b501`](https://github.com/jhugon/semantic-data-taking-webapp/commit/b15b501dc01e0fc6c719dce4612eb477e17d7012) Got RDF dataset working better
- [`253bead`](https://github.com/jhugon/semantic-data-taking-webapp/commit/253beade1e6ae47a31530358a48c1609b5dddbf2) Now select out the graph from the dataset better
- [`23d7fc4`](https://github.com/jhugon/semantic-data-taking-webapp/commit/23d7fc45aed9abe2fd8370ec2298eef0545d9aea) Working on converting db.py to use rdf datasets
- [`c15544c`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c15544c1f418db6bfa8eff1d6e52291308df9c9c) working on making rdflib work with jena-fuseki
- [`e5557d2`](https://github.com/jhugon/semantic-data-taking-webapp/commit/e5557d2e948c4c904c3f301d46063626e24c2178) got log info working in db.py __main__
- [`2efa8cb`](https://github.com/jhugon/semantic-data-taking-webapp/commit/2efa8cbeab7575bfe9c61e2de139a80b4e6dbcc6) trying to make initialize db work with sparql server
- [`1ee5b21`](https://github.com/jhugon/semantic-data-taking-webapp/commit/1ee5b217766bd5a0867091c729946297cde7e594) Working on adding Apache Jena Fuseki SPARQL Server
- [`69ddde2`](https://github.com/jhugon/semantic-data-taking-webapp/commit/69ddde25f8f40518a7d72fc73c3d628ab5655205) added options to configure RDF DB type
- [`4c888ab`](https://github.com/jhugon/semantic-data-taking-webapp/commit/4c888ab66ae6c6ecf7c4db13652bfc544ffa859c) Added manual db init, resolves #19
- [`4610195`](https://github.com/jhugon/semantic-data-taking-webapp/commit/4610195edfebc3e77de028b5edc0f61985d92d5d) Do things as user semweb in Dockerfiles
- [`a7e9a7d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a7e9a7ddd4cf1adca062f59aafb14a0c9fcf6142) cloudbuild: think I have the submodule URL correct now
- [`6771ff9`](https://github.com/jhugon/semantic-data-taking-webapp/commit/6771ff948d48d375d0ca11e4bc81c376acf3369b) cloudbuild: trying now with Google Source repo
- [`8f452da`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8f452dab53e0fb2dce49b742d6ced1fbe50d1a8f) Try adding git submodule update
- [`8534dcd`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8534dcdcb4753d39d53af489624a4cad8b29eac3) Try to run git submodule init in cloudbuild
- [`6a97b5d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/6a97b5d0f470e16383e4a779f961ba7c0455e541) still debugging cloudbuild
- [`5eed8e1`](https://github.com/jhugon/semantic-data-taking-webapp/commit/5eed8e139307b253ff6fb928a52bd657f50450a5) Add git submodule init to cloudbuild.yaml
- [`085a8e5`](https://github.com/jhugon/semantic-data-taking-webapp/commit/085a8e57481673222a492006998933d1a5a0b94e) added cloudbuild.yaml file (still debugging cloudbuild)
- [`36329d0`](https://github.com/jhugon/semantic-data-taking-webapp/commit/36329d044af4c76b6c7461d0478993da1127c2c3) more cloudrun build debugging
- [`8d3b06a`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8d3b06a6d15240c2744f8116a8db8ec0856ec3de) Trying to debug Dockerfile.cloudrun
- [`522816f`](https://github.com/jhugon/semantic-data-taking-webapp/commit/522816fe5e6bded5b355eb55b8eeb965bc83113b) Added Dockerfile.cloudrun, preparing for Google Cloud Run
- [`efbea4e`](https://github.com/jhugon/semantic-data-taking-webapp/commit/efbea4eb02c63d356550ca93229a905e0114e011) updated README with Docker instructions
- [`676d9f6`](https://github.com/jhugon/semantic-data-taking-webapp/commit/676d9f641bc9d826d5b3b56fda2587bbd574f3b8) Merge pull request #18 from jhugon/add_app_configuration
- [`ebd9597`](https://github.com/jhugon/semantic-data-taking-webapp/commit/ebd959722fb47a5ec519c1eac03cada704f8219b) Can now update flask config with file or env vars
- [`51ad252`](https://github.com/jhugon/semantic-data-taking-webapp/commit/51ad252c9f7ed3276da2488d0ac564d496014a13) added configurable RDF data and user URIs for #17
- [`99fb3df`](https://github.com/jhugon/semantic-data-taking-webapp/commit/99fb3df5c87dd5d2b37e7623238e299c314c8a85) Got configurable flask server hostname working for #7
- [`a1b9e0b`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a1b9e0b939184aaffb6e9be9fa1c914116651a5f) Added configuration params for path to DB and user file
- [`c75bc30`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c75bc30f810ddcc6779327d7c29f5e9c4523fd36) Now log flask configuration
- [`b89b197`](https://github.com/jhugon/semantic-data-taking-webapp/commit/b89b19784aadd37e9510bfba6e64bb175758be13) Merge pull request #16 from jhugon/docker
- [`3c5fb26`](https://github.com/jhugon/semantic-data-taking-webapp/commit/3c5fb26be2789ec513bf2ab372944969345ee4b3) nginx: made hostname configurable with an env var
- [`274b445`](https://github.com/jhugon/semantic-data-taking-webapp/commit/274b445276a2c998bb23bd49c1aea51e13f9be75) Got nginx config.d/default.conf working
- [`514c7eb`](https://github.com/jhugon/semantic-data-taking-webapp/commit/514c7ebb49c7b929e1418f3096ec4ecd5e7a1444) simplified nginx.conf
- [`dc4e961`](https://github.com/jhugon/semantic-data-taking-webapp/commit/dc4e9611185cf46569efd3e663e5c99893e93d1d) nginx working
- [`0f11cb6`](https://github.com/jhugon/semantic-data-taking-webapp/commit/0f11cb6b2b7d9c05779a8299a0b16de166b40250) working on nginx Docker config
- [`8c80c14`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8c80c140796d1093108c4fd5ad7b810e57228678) Docker uses Gunicorn now, but with an issue with worker timeouts
- [`fb894d6`](https://github.com/jhugon/semantic-data-taking-webapp/commit/fb894d65bdee993102adcef2a22181338745cd54) Added a Dockerfile
- [`e66ea98`](https://github.com/jhugon/semantic-data-taking-webapp/commit/e66ea98d82b0c1efe90418a561fe5ec01c536fc6) Merge pull request #8 from jhugon/flask-simple-login
- [`d671341`](https://github.com/jhugon/semantic-data-taking-webapp/commit/d671341e7d65c368f90fd71483212ba32683a4fd) Working on connecting login user to DB user #3
- [`ece53a3`](https://github.com/jhugon/semantic-data-taking-webapp/commit/ece53a3bc851d14cdd10b762e05f812150d15be6) Do some bootstrap styling
- [`b3badc1`](https://github.com/jhugon/semantic-data-taking-webapp/commit/b3badc150eff790f332f2972409f8c8ea9f5b285) Updated to use new templates for all pages
- [`f1ab267`](https://github.com/jhugon/semantic-data-taking-webapp/commit/f1ab267c0d4a528c139c3c8eb128d8f0168f7f08) working on using flask-simple-login
- [`ee5fb6d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/ee5fb6d013188fd0e6d3d44eac421f9c160dde22) Added some templates from flask-simple-login
- [`567aef1`](https://github.com/jhugon/semantic-data-taking-webapp/commit/567aef11d1b51e7b2e122f06bf6a11f5786a0ac6) Updated things for Python 3.10
- [`8508cb7`](https://github.com/jhugon/semantic-data-taking-webapp/commit/8508cb7211fea3da3e584f25f2426d7660edd2d1) Added fuel economy and fuel price QKs and units
- [`91608db`](https://github.com/jhugon/semantic-data-taking-webapp/commit/91608dbaa74cc294b8b585b9001b238673264ea3) hints on quantity kinds
- [`c9f48db`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c9f48db86d39fb1c537ed33041e9ced912c969ef) persistent DB is working
- [`e8526b9`](https://github.com/jhugon/semantic-data-taking-webapp/commit/e8526b9b786bf4a9f2e0022bb8399dbe9134d98a) working on BerkeleyDB store for graph DB
- [`a2ae479`](https://github.com/jhugon/semantic-data-taking-webapp/commit/a2ae479cbc0f141f2fa42c2405c2cfa33e52ad44) Add a little server-side validation to QK and unit
- [`06f3cb2`](https://github.com/jhugon/semantic-data-taking-webapp/commit/06f3cb266122b44ecbc7fd8f7a6b847b0552388a) Got status to show up on Add Property
- [`4cd981d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/4cd981d61838104d2329b8b65b837efceb7da6b5) Adding properties seems to work now
- [`4cc83cf`](https://github.com/jhugon/semantic-data-taking-webapp/commit/4cc83cfdbff6327f91b96f3804c1208b91b91b0e) redid quantityKind/Unit lists in db.py
- [`88f65dc`](https://github.com/jhugon/semantic-data-taking-webapp/commit/88f65dc020cb9edb7291f5b32643fb92d5bca5f6) working on add property web
- [`481339d`](https://github.com/jhugon/semantic-data-taking-webapp/commit/481339d0721b9c2bb0f56439356f0f8d95542e89) Added addproperty page, not yet functional
- [`9bc33b5`](https://github.com/jhugon/semantic-data-taking-webapp/commit/9bc33b5bec170cb427df8ebdb9725a95983d4277) web can now add features
- [`87a7f66`](https://github.com/jhugon/semantic-data-taking-webapp/commit/87a7f66eee89005132f5f98325923cbb366095be) deal with some data validation errors
- [`c2e6caa`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c2e6caa0519555828d773d3e72002ba9b9ed882a) added web interface to basic data entry
- [`7771d30`](https://github.com/jhugon/semantic-data-taking-webapp/commit/7771d30563569036c0e717394a3aaf3261e2d442) db: added enterData method
- [`0401330`](https://github.com/jhugon/semantic-data-taking-webapp/commit/040133052972da573f64f20ff487833690821544) working on data entry db methods
- [`cbd8559`](https://github.com/jhugon/semantic-data-taking-webapp/commit/cbd85593bcd8acbe3895569a6c222cd0922fdd8b) table viewing on web working
- [`1d0a51f`](https://github.com/jhugon/semantic-data-taking-webapp/commit/1d0a51fa14ce117236f6e18330b4960df5016326) starting on Flask web part
- [`c0da7ac`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c0da7ac9d4e9a3407941216b9e76392efa601d5e) added get_data method to db.py
- [`c94ff6a`](https://github.com/jhugon/semantic-data-taking-webapp/commit/c94ff6aba51d8507a6e603c8610f4eabb4ec3385) Added getColumnHeadings to db.py
- [`190976f`](https://github.com/jhugon/semantic-data-taking-webapp/commit/190976fff3e5179464ef7cc8cc91641ff55f71b1) working on things
- [`9aec606`](https://github.com/jhugon/semantic-data-taking-webapp/commit/9aec60604422579511363ca1d853558fcebe72f1) fixed and extended car-extended.ttl
- [`335ac9e`](https://github.com/jhugon/semantic-data-taking-webapp/commit/335ac9e704979e090e634dea5a70ed38d1667cfc) working on car-example.ttl
- [`11c7ae7`](https://github.com/jhugon/semantic-data-taking-webapp/commit/11c7ae7d44e70dec3c9662d4830159123d5a81f3) updated ontology to not make subclasses, just some properties
- [`226e5e8`](https://github.com/jhugon/semantic-data-taking-webapp/commit/226e5e8dea0efdf8bab185eb40968a6c4608293a) Added sample.ttl
- [`1ffed81`](https://github.com/jhugon/semantic-data-taking-webapp/commit/1ffed81d56c776538f8ccb7be5940574ee260c48) initial draft of ontology/sdtw.owl complete
- [`0cd5e13`](https://github.com/jhugon/semantic-data-taking-webapp/commit/0cd5e1387695d8c554c4f135d583fd80dde43929) added PipFiles and ontology/sdtw.owl
- [`218a323`](https://github.com/jhugon/semantic-data-taking-webapp/commit/218a32394fd5dc99cc0a2d0c2789bfe36cb8bffb) Update README.md
- [`8992551`](https://github.com/jhugon/semantic-data-taking-webapp/commit/89925516a153ad86a162423f797a084cdb1ac6c5) Initial commit
