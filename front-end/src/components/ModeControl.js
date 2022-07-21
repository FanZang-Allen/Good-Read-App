import React from 'react';
import GetMode from './GetMode';
import PutMode from './PutMode';
import PostMode from './PostMode';
import DeleteMode from './DeleteMode';

const ModeControl = ({ mode }) => {
    switch(mode) {
        case 'get':
            return (
                <div>
                <GetMode/>
                </div>
            )
        case 'put':
            return (
                <div>
                <PutMode/>
                </div>
            )
        case 'post':
            return (
                <div>
                <PostMode/>
                </div>
            )
        case 'delete':
            return (
                <div>
                <DeleteMode/>
                </div>
            )
        default:
            return (
                <div>
                <h4 style={{margin:'10px', color:'white'}}> Please click a button.</h4>
                </div>
            )
    }
}

export default ModeControl
