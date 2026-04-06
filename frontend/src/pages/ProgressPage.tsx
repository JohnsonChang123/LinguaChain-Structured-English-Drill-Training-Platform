import { useEffect, useState } from 'react'

import { ProgressItem, getMyProgress } from '../lib/api'

export function ProgressPage() {
  const [items, setItems] = useState<ProgressItem[]>([])

  useEffect(() => {
    getMyProgress()
      .then((res) => setItems(res.items))
      .catch(console.error)
  }, [])

  return (
    <div className="max-w-3xl mx-auto mt-10 p-4 space-y-4">
      <h1 className="text-2xl font-bold">My Progress</h1>
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.lesson_id} className="rounded-xl border bg-white p-4">
            <h2 className="font-semibold">{item.lesson_title}</h2>
            <p className="text-sm">Completion rate: {(item.completion_rate * 100).toFixed(0)}%</p>
            <p className="text-sm">Average score: {item.average_score.toFixed(2)}</p>
          </div>
        ))}
        {items.length === 0 && <p className="text-sm text-slate-600">No progress yet. Do some drills first.</p>}
      </div>
    </div>
  )
}
