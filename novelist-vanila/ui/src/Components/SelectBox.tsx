// import { useState } from "react"

interface SelectBoxProp {
  label: string
  setSelectBox: any
}

export default function SelectBox({ label, setSelectBox }: SelectBoxProp) {  
  return (
    <div className="flex flex-col m-2 p-3 border-solid border-2 w-2/4 rounded-lg">
      <div className="flex ml-2">{label}</div>
      <select
        className="m-2 bg-slate-200 rounded-md focus:outline-none"
        onChange={setSelectBox}
      >
        <option value=''>-- 선택하세요 --</option>
        <option value='action'>액션</option>
        <option value='thriller'>스릴러</option>
        <option value='romance'>로맨스</option>
        <option value='SF'>SF</option>
      </select>
    </div>
  )
}