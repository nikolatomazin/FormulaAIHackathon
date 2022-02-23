import './App.css';
import Predict from './Predict';
import MyDocumentation from './MyDocumentation';
import Nav from './Nav';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Nav />
        <Switch>
          <Route path="/predict" component={Predict}/>
          <Route path="/documentation" component={MyDocumentation}/>
        </Switch>
      </div>
    </Router>
  );
}

export default App;
