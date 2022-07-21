import React from 'react';
import * as d3 from "d3";
import './Components.css';
import './TopK.css';
import ErrorMessage from './ErrorMessage';
import { useState } from "react";

const TopKAuthors = () => {

    let [errorMessage, setMessage] = useState('');

    async function showClick(event) {
        event.preventDefault();
        let Knum = document.getElementById('inputK').value;
        let data = []
        try {
            let response = await fetch(`http://127.0.0.1:5000/api/top/author?k=${Knum}`, {
                method: 'Get'
            });
            if (response.status !== 200) {
                let error_data = await response.json();
                setMessage(error_data['error_message']);
            } else {
                let query_data = await response.json();
                data = query_data['Query Result']
            }
        } catch(e) {
            setMessage('Connection failed.');
            console.log(e);
        }
        data.forEach(d => {
            d['rating'] = +d['rating']
        })
        const arr_length = data.length;
        setMessage(`Top ${arr_length} Authors:`);
        render(data);
    }

    const render = (data) => {
        const arr_length = data.length;

        const svg = d3.select('svg');
        svg.selectAll('rect').remove();
        svg.selectAll('g').remove();
        const width = +svg.attr('width');
        const height= 300 + 10 * arr_length;
        const xValue = d => d['rating'];
        const yValue = d => d['name'];
        const margin = {top: 20, right: 20, bottom: 20, left: 150};
        const innerWidth = width - margin.left - margin.right;
        const innerHeight = height - margin.top - margin.bottom;

        const xScale = d3.scaleLinear().domain([d3.min(data,xValue) - 0.1, d3.max(data,xValue)]).range([0,innerWidth]);
        const yScale = d3.scaleBand().domain(data.map(yValue)).range([0,innerHeight]).padding(0.1);

        const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

        g.append('g').call(d3.axisLeft(yScale));
        g.append('g').call(d3.axisBottom(xScale)).attr('transform', `translate(0, ${innerHeight})`);
        g.selectAll('rect').data(data).enter().append('rect')
        .attr('y', d => yScale(yValue(d))).attr('width', d=> xScale(xValue(d))).attr('height', d => yScale.bandwidth())

    }

    return (
        <div className='VerticalCenterContainer'>
            <form className="InputHolder">
                <div className="Input">
                    <button style={{backgroundColor: 'blue'}} className='GoButton'>
                        <a href="/api" className="href">
                            Go Back
                        </a>
                    </button>
                    <input
                        type='text'
                        placeholder='Please enter a number'
                        id = 'inputK'
                    />
                    <button style={{backgroundColor: 'green'}} className='GoButton' onClick={showClick}>Show</button>
                </div>
            </form>
            <div id='errorMessage'><ErrorMessage message={errorMessage}/></div>
            <svg width="800" height = "1500" id='barChart'>
            </svg>
        </div>
    )
}

export default TopKAuthors
