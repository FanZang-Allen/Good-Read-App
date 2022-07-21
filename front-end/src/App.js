import Header from "./components/Header";
import ApiButton from "./components/ApiButton";
import ModeControl from "./components/ModeControl";
import TopKBooks from "./components/TopKBooks";
import TopKAuthors from "./components/TopKAuthors";
import { BrowserRouter as Router, Route } from "react-router-dom";
import { useState } from "react";
import './App.css';


function App() {
  let [mode, setMode] = useState('null')

  const getClick = () => setMode('get');
  const putClick = () => setMode('put');
  const postClick = () => setMode('post');
  const deleteClick = () => setMode('delete');

  return (
    <Router>
      <div className='App'>
        <Header/>
        <Route path='/api' render={(props) => (
          <>
          <ApiButton getClick={getClick} putClick={putClick} postClick={postClick} deleteClick={deleteClick}/>
          <ModeControl mode={mode}/>
          </>
        )
        }/>
        <Route path='/vis/top-books' component={TopKBooks}/>
        <Route path='/vis/top-authors' component={TopKAuthors}/>
      </div>
    </Router>
  );
}

export default App;
