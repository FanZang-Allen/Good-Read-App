import React from 'react'
import './Components.css';
//import 'bootstrap/dist/css/bootstrap.css'
import ErrorMessage from './ErrorMessage';
import { DropdownButton } from 'react-bootstrap';
import { Dropdown } from 'react-bootstrap';
import { useState } from "react";
import AuthorList from './AuthorList';
import BookList from './BookList';


const GetMode = () => {

    let [collectionName, setCollection] = useState('Pick a collection');
    let [logicOperator, setLogic] = useState('Logic');
    let [errorMessage, setMessage] = useState('');
    let [author_info_list, setAuthorInfo] = useState([]);
    let [book_info_list, setBookInfo] = useState([]);

    const CollectionSelect=(e)=>{
        setCollection(e)
        if(e === 'book'){
            console.log('book serach');
        } else if (e === 'author') {
            console.log('author serach');
        }
    }

    const LogicSelect=(e)=>{
        setLogic(e);
        if (e === 'AND' || e === 'OR') {
            document.getElementById('SecondQuery').style.display = '';
        } else {
            document.getElementById('SecondQuery').style.display = 'none';
        }
    }

    const ShowMessage = (message) => {
        document.getElementById('errorMessage').style.display='';
        setMessage(message);
    }

    async function SearchById(event) {
        event.preventDefault();
        setAuthorInfo([]);
        setBookInfo([]);
        let gotID = document.getElementById('inputID').value;
        if (gotID === '') {
            ShowMessage('Please enter a ID');
            return
        }
        if (collectionName === 'Pick a collection') {
            ShowMessage('Please pick a collection');
            return
        }
        try {
            let response = await fetch(`http://127.0.0.1:5000/api/${collectionName}?id=${gotID}`, {
                method: 'GET'
            });
            if (response.status !== 200) {
                let error_data = await response.json();
                ShowMessage(error_data['error_message']);
            } else {
                let query_data = await response.json();
                ShowMessage('Search Result:');
                if (collectionName === 'book') {
                    setBookInfo(query_data['Query Result']);
                } else {
                    setAuthorInfo(query_data['Query Result']);
                }
            }
        } catch(e) {
            ShowMessage('Connection failed.');
            console.log(e);
        }
    }

    async function SearchByQuery(event) {
        event.preventDefault();
        setAuthorInfo([]);
        setBookInfo([]);
        let firstObject = document.getElementById('FirstObject').value;
        let firstField = document.getElementById('FirstField').value;
        let firstContent = document.getElementById('FirstContent').value;
        let secondObject = document.getElementById('SecondObject').value;
        let secondField = document.getElementById('SecondField').value;
        let secondContent = document.getElementById('SecondContent').value;
        let query_str = '';
        if (logicOperator === 'AND' || logicOperator === 'OR') {
            query_str += `${firstObject}.${firstField}:${firstContent} ${logicOperator}`;
            query_str += `${secondObject}.${secondField}:${secondContent}`
        } else if (logicOperator === 'NOT') {
            query_str += `${firstObject}.${firstField}:${logicOperator} ${firstContent}`;
        } else {
            query_str += `${firstObject}.${firstField}:${firstContent}`;
        }
        try {
            let response = await fetch(`http://127.0.0.1:5000/api/search?q=${query_str}`, {
                method: 'Get'
            });
            if (response.status !== 200) {
                let error_data = await response.json();
                ShowMessage(error_data['error_message']);
            } else {
                let query_data = await response.json();
                ShowMessage('Search Result:');
                if (firstObject === 'book') {
                    setBookInfo(query_data['Query Result']);
                } else {
                    setAuthorInfo(query_data['Query Result']);
                }
            }
        } catch(e) {
            ShowMessage('Connection failed.');
            console.log(e);
        }
    }


    return (
        <div className='VerticalCenterContainer'>
            <h1 className='Header'style = {{margin: 10}}> Search by Id</h1>
            <form className="InputHolder">
                <div className="Input">
                    <DropdownButton variant="success" title={collectionName} onSelect={CollectionSelect}>
                        <Dropdown.Item eventKey="book">Book</Dropdown.Item>
                        <Dropdown.Item eventKey="author">Author</Dropdown.Item>
                    </DropdownButton>
                    <input
                        type='text'
                        placeholder='Please enter a ID'
                        id = 'inputID'
                    />
                    <button style={{backgroundColor: 'green'}} className='GoButton' onClick={SearchById}>Go</button>
                </div>
            </form>
            <h1 className='Header' style = {{margin: 20}}> Search Database</h1>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString' > Object:</h2>
                    <input
                        type='text'
                        style = {{"width": "10%"}}
                        id = 'FirstObject'
                    />
                    <h2 className='QueryArgString' > Field:</h2>
                    <input
                        type='text'
                        style = {{"width": "10%"}}
                        id = 'FirstField'
                    />
                    <h2 className='QueryArgString'> Content:</h2>
                    <input
                        type='text'
                        style = {{"width": "15%"}}
                        id = 'FirstContent'
                    />
                    <DropdownButton variant="primary" title={logicOperator} onSelect={LogicSelect}>
                        <Dropdown.Item eventKey="Logic"></Dropdown.Item>
                        <Dropdown.Item eventKey="NOT">NOT</Dropdown.Item>
                        <Dropdown.Item eventKey="AND">AND</Dropdown.Item>
                        <Dropdown.Item eventKey="OR">OR</Dropdown.Item>
                    </DropdownButton>
                </div>
            </form>
            <form className="InputHolder" id="SecondQuery" style={{'display':'none'}}>
                <div className="Input">
                    <h2 className='QueryArgString' > Object:</h2>
                    <input
                        type='text'
                        style = {{"width": "10%"}}
                        id = 'SecondObject'
                    />
                    <h2 className='QueryArgString' > Field:</h2>
                    <input
                        type='text'
                        style = {{"width": "10%"}}
                        id = 'SecondField'
                    />
                    <h2 className='QueryArgString'> Content:</h2>
                    <input
                        type='text'
                        style = {{"width": "15%"}}
                        id = 'SecondContent'
                    />
                    <DropdownButton variant="primary" title={logicOperator} style={{'visibility':'hidden'}}>
                    </DropdownButton>
                </div>
            </form>
            <button style={{"backgroundColor": 'green', "width": "150px", "margin": "12px"}} className='GoButton' onClick={SearchByQuery}>Search</button>
            <div id='errorMessage' style={{'display':'none'}}><ErrorMessage message={errorMessage}/></div>
            <AuthorList infolist={author_info_list}/>
            <BookList infolist={book_info_list}/>
        </div>
        
    )
}

export default GetMode
