import React from 'react'
import Author from './Author'

const AuthorList = ({ infolist }) => {
    return (
        <>
        {infolist.map((info) => (
            <Author data={info}/>
        ))}
        </>
    )
}

export default AuthorList
