import React, { useState } from 'react';
import './App.css';
import InputBox from './Components/InputBox';
import SelectBox from './Components/SelectBox';

function App() {
  // textbox
  const [ genre_text, setGenre ] = useState('')
  const [ characters_text, setCharacters ] = useState('')
  const [ news_text, setNews ] = useState('')

  function setGenreText(e: any) {
    setGenre(e.target.value)
  }

  function setCharactersText(e: any) {
    setCharacters(e.target.value)
  }

  function setNewsText(e: any) {
    setNews(e.target.value)
  }

  // result
  const [ result_text, setResult ] = useState("")

  // async function postData(url: string, data: any): Promise<string> {
  //   // 옵션 기본 값은 *로 강조
  //   const response = await fetch(url, {
  //     method: "POST", // *GET, POST, PUT, DELETE 등
  //     mode: "cors", // no-cors, *cors, same-origin
  //     cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
  //     credentials: "same-origin", // include, *same-origin, omit
  //     headers: {
  //       "Content-Type": "application/json",
  //       // 'Content-Type': 'application/x-www-form-urlencoded',
  //     },
  //     // redirect: "follow", // manual, *follow, error
  //     // referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
  //     body: JSON.stringify(data), // body의 데이터 유형은 반드시 "Content-Type" 헤더와 일치해야 함
  //   });
  //   return JSON.stringify(response.json()); // JSON 응답을 네이티브 JavaScript 객체로 파싱
  // }

  const buttonClick3 = async (e: any) => {
    const data = {
      genre: genre_text,
      characters: characters_text,
      news_text: news_text
    }
    const res = await fetch("http://localhost:8000/test", {
      method: "POST",
      mode: "cors",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
    const result = await res.json()
    setResult(JSON.stringify(result))
  }

  return (
  <>
    <div className='container'>
      <div className='flex flex-col items-center'>
        <SelectBox 
          label='장르'
          setSelectBox={setGenreText}
        />
        <InputBox 
          label='등장인물'
          inputText={characters_text}
          setInputText={setCharactersText}
        />
        <InputBox 
          label='뉴스기사'
          inputText={news_text}
          setInputText={setNewsText}
        />

        <button 
          className='bg-emerald-200 p-2 rounded-lg' 
          onClick={(e) => buttonClick3(e)}
        >Submit</button>
        <div className='box'><p>{result_text}</p></div>
      </div>

    </div>
  </>
  );
}

export default App;
