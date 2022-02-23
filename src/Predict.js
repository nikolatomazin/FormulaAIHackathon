import logo from './components/logo.svg';
import React from 'react';
import Button from '@mui/material/Button';
import { TextField } from '@mui/material';
import './Predict.css';
import { useState } from "react";
import f1sound from './components/sound.wav'
import axios from 'axios';

 function Predict() {
  const [data, setdata] = useState("");

  const handleSubmit = async (event) => {
    var body = {
      // data: event.target[0].value
      input_data: event.target[0].value
  };
  
    const audio = new Audio(f1sound);
    audio.play();
    event.preventDefault();
    
    let res
    let formData = new FormData();
    formData.append('input_data', event.target[0].value);

    axios
      .post(`http://141.144.224.177:5000/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(res => {
        var elem = document.getElementById('output');
        let strespons = res.data.predictions;
        strespons = strespons.replace("]", "")
        strespons = strespons.replace("[", "")
        strespons = strespons.replace(/\'/g, "\"")
        console.log(strespons)
        // strespons = strespons.slice(1, -1);
        elem.value = JSON.stringify(JSON.parse(strespons), null, 2)
        console.log(res.data)
      })
      .catch(err => console.log(err));

    // try {
    //   let formData = new FormData();
    //   formData.append('input_data', event.target[0].value);
    //   let res = await fetch("http://141.144.224.177:5000/predict", {
    //     method: "POST",
    //     body: JSON.stringify({
    //       "input_data": event.target[0].value
    //     }),
    //     headers: {'Content-Type': 'multipart/form-data'},
        
    //   });
    //   let resJson = await res.json();
    //   if (res.status === 200) {
    //     alert("super")
    //   } else {
    //     alert("nista")
    //     // setMessage("Some error occured");
    //   }
    // } catch (err) {
    //   console.log(err);
    // }
  }
  

  return(
    <div className="AppPredict">
        <img src={logo} className="App-logo" alt="logo" />
          <div className="infoText">
          Paste one or multiple raw csv rows in this form.
          </div>
          <p>Output:</p>
        <TextField
            id="output"
            multiline
            inputMode='textArea'
            className="outputField"
            style = {{width: 500}}
            variant="filled"
            color="secondary"
          />
        <form onSubmit={handleSubmit} className="csvForm">
          <TextField //OVO TU OVDJE
            multiline
            inputMode='textArea'
            className="csvField"
            style = {{width: 500}}
            variant="filled"
            color="secondary"
            onChange={(e) => setdata(e.target.value)}
          />
          <Button type="submit" color="primary" variant="filled" textcolor="blue">Predict</Button>
        </form>
       
    </div>
  );
}

export default Predict;