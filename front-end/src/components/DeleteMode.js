import React from 'react'
import './Components.css';
import ErrorMessage from './ErrorMessage';
import { DropdownButton } from 'react-bootstrap';
import { Dropdown } from 'react-bootstrap';
import { useState } from "react";


const DeleteMode = () => {

    let [collectionName, SetCollection] = useState('Pick a collection');
    let [errorMessage, SetMessage] = useState('');

    const CollectionSelect=(e)=>{
        SetCollection(e)
    }

    const ShowMessage = (message) => {
        document.getElementById('errorMessage').style.display='';
        SetMessage(message);
    }

    async function DeleteById(event) {
        event.preventDefault();
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
                method: 'DELETE'
            });
            if (response.status !== 200) {
                let error_data = await response.json();
                ShowMessage(error_data['error_message']);
            } else {
                let response_data = await response.json();
                ShowMessage(response_data['Response']);
            }
        } catch(e) {
            ShowMessage('Connection failed.');
            console.log(e);
        }
    }

    return (
        <div className='VerticalCenterContainer'>
            <h1 className='Header'style = {{margin: 10}}> Delete by Id</h1>
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
                    <button style={{backgroundColor: 'red', width:'100px'}} className='GoButton' onClick={DeleteById}>Delete</button>
                </div>
            </form>
            <div id='errorMessage' style={{'display':'none'}}><ErrorMessage message={errorMessage}/></div>
        </div>
    )
}

export default DeleteMode
