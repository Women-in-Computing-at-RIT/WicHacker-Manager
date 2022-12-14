# Testing Dev Notes #
* Tests must be run from /src directory
  * Run tests using 'python3 -m pytest'
  * Can also use runUnitTests.sh script
  * Running from /src directory allows mock routes to be standardized
* I know the controller unit tests are not true unit tests
  * Feel free to refactor these later
  * It was quicker on initial development to do quasi integration tests than full unit tests for everything
* The api client can be imported from testSetupHelper
  * The import will show as not used, leave it in as a side effect and python will be able to resolve it
* Mocking, @patch and funny business
  * @patch allows you to inject a unittest Mock object into your code
  * the path involves the file followed by the called function you wish to mock
  * the mock object is then passed as a parameter
  * If using multiple @patch annotations, the one directly above the function is the first argument proceeding up the list
  * can use @patch(<path>, side_effect=<Insert Exception>) for testing exceptions
  * to set a return value of a mocked function use 'mock.return_value = x'
  * the exception handling for auth errors on the mocked api is wonky
  * make sure to mock authentication for all protected endpoints
    * all you need to do is return a dictionary with the key "sub" from the authentication method call
    * ex: 'mock_authenticate.return_value = {"sub": "testAuth0ID"}'
  * i've been using the built in python assertions, feel free to refactor if there's an assertion package you feel strongly about

### Github Actions ###
There's a github actions job on all pushes that will run pytest. We can't merge unless all tests are passing

### And Finally... ###
I know tests are tedious, but taking the time to write tests will save us a lot of time later debugging
or catching errors we didn't even know we had
