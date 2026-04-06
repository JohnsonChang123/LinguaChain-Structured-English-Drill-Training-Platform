import { FormEvent, useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'

import { SourceAttribution } from '../components/SourceAttribution'
import { Drill, Lesson, getLesson, getLessonDrills, submitAttempt } from '../lib/api'

export function LessonPage() {
  const { lessonId } = useParams()
  const id = Number(lessonId)
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [drills, setDrills] = useState<Drill[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [input, setInput] = useState('')
  const [feedback, setFeedback] = useState('')

  useEffect(() => {
    if (!id) return
    getLesson(id).then(setLesson).catch(console.error)
    getLessonDrills(id).then(setDrills).catch(console.error)
  }, [id])

  const currentDrill = useMemo(() => drills[currentIndex], [drills, currentIndex])

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    if (!currentDrill) return

    const result = await submitAttempt(currentDrill.id, input)
    setFeedback(result.is_correct ? 'Correct ✅' : `Incorrect ❌ Expected: ${String(result.feedback.expected)}`)
    setInput('')
  }

  function onNext() {
    setFeedback('')
    setCurrentIndex((idx) => Math.min(idx + 1, drills.length - 1))
  }

  if (!lesson || !currentDrill) {
    return <div className="p-6">Loading lesson...</div>
  }

  return (
    <div className="max-w-3xl mx-auto mt-8 p-4 space-y-5">
      <h1 className="text-2xl font-bold">{lesson.title}</h1>
      <p className="p-3 rounded border bg-white">Transcript: {lesson.transcript}</p>

      <SourceAttribution
        sourceName={lesson.source_name}
        sourceUrl={lesson.source_url}
        licenseName={lesson.license_name}
        licenseUrl={lesson.license_url}
        attributionText={lesson.attribution_text}
      />

      <div className="rounded-xl border bg-white p-4 space-y-2">
        <p className="text-sm text-slate-600">
          Drill {currentIndex + 1} / {drills.length}
        </p>
        <p><strong>Type:</strong> {currentDrill.drill_type}</p>
        <p><strong>Prompt:</strong> {currentDrill.prompt_text}</p>
        <p><strong>Base sentence:</strong> {currentDrill.base_sentence}</p>

        <form onSubmit={onSubmit} className="space-y-2">
          <input className="w-full border rounded p-2" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type your answer" />
          <button className="bg-green-600 text-white px-4 py-2 rounded" type="submit">Submit</button>
        </form>

        {feedback && <div className="rounded border p-2 bg-slate-50">{feedback}</div>}

        <button onClick={onNext} className="underline text-sm">Next drill</button>
      </div>
    </div>
  )
}
