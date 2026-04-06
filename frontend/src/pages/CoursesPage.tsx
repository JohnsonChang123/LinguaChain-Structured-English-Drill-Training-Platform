import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { Course, getCourses } from '../lib/api'

export function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([])

  useEffect(() => {
    getCourses().then(setCourses).catch(console.error)
  }, [])

  return (
    <div className="max-w-3xl mx-auto mt-10 p-4 space-y-4">
      <h1 className="text-2xl font-bold">Courses</h1>
      <div className="grid gap-3">
        {courses.map((course) => (
          <div key={course.id} className="p-4 rounded-xl border bg-white">
            <h2 className="font-semibold">{course.title}</h2>
            <p className="text-sm">Level: {course.cefr_level}</p>
            <p className="text-sm text-slate-600">{course.description}</p>
            <Link className="underline text-sm mt-2 inline-block" to="/lessons/1">
              Open seeded lesson
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}
