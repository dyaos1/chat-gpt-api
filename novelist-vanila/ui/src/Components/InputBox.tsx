import { useState } from "react"

interface InputBoxProp {
  label: string
  inputText: string
  setInputText: any
}

export default function InputBox({ label, setInputText }: InputBoxProp) {  
  return (
    <div className="flex flex-col m-2 p-3 border-solid border-2 w-2/4 rounded-lg">
      <div className="flex ml-2">{label}</div>
      <input 
        type="text" 
        className="p-2 m-2 bg-slate-200 rounded-md focus:outline-none"
        onChange={setInputText}
      />
    </div>
  )
}