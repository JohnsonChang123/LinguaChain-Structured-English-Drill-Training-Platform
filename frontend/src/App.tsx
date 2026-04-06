import { Link, Navigate, Route, Routes } from 'react-router-dom'

import { CoursesPage } from './pages/CoursesPage'
import { LessonPage } from './pages/LessonPage'
import { LoginPage } from './pages/LoginPage'
import { ProgressPage } from './pages/ProgressPage'

function TopNav() {
  return (
    <nav className="bg-white border-b">
      <div className="max-w-4xl mx-auto p-3 flex gap-4 text-sm">
        <Link className="underline" to="/login">Login</Link>
        <Link className="underline" to="/courses">Courses</Link>
        <Link className="underline" to="/progress">Progress</Link>
      </div>
    </nav>
  )
}

export default function App() {
  return (
    <>
      <TopNav />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/courses" element={<CoursesPage />} />
        <Route path="/lessons/:lessonId" element={<LessonPage />} />
        <Route path="/progress" element={<ProgressPage />} />
      </Routes>
    </>
  )
}
