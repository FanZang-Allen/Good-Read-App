import React from 'react'
import './Components.css';
import 'bootstrap/dist/css/bootstrap.css'
// import DropdownButton from 'react-bootstrap/DropdownButton';
// import Dropdown from 'react-bootstrap/Dropdown';
import { DropdownButton } from 'react-bootstrap';
import { Dropdown } from 'react-bootstrap';


const ApiButton = ({ getClick, putClick, postClick, deleteClick }) => {
    return (
    <div className='ApiButtonHolder'>
        <button style={{backgroundColor: 'green'}} className='ApiButton' onClick={getClick}>Get</button>
        <button style={{backgroundColor: 'blue'}}className='ApiButton' onClick={putClick}>Put</button>
        <button style={{backgroundColor: 'gray'}}className='ApiButton' onClick={postClick}>Post</button>
        <button style={{backgroundColor: 'red'}}className='ApiButton' onClick={deleteClick}>Delete</button>
        <DropdownButton variant="success" title='Top K' size="lg" style={{"width": "20%", "height":"calc(70px + 1vmin)"}}>
            <Dropdown.Item eventKey="book" href="/vis/top-books">Book</Dropdown.Item>
            <Dropdown.Item eventKey="author" href="/vis/top-authors">Author</Dropdown.Item>
        </DropdownButton>
    </div>
    )
}

export default ApiButton
