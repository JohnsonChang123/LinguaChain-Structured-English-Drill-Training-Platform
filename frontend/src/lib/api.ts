const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export type Course = {
  id: number
  title: string
  cefr_level: string
  description: string
}

export type Lesson = {
  id: number
  title: string
  transcript: string
  audio_url: string
  source_name: string
  source_url: string
  license_name: string
  license_url: string
  attribution_text: string
}

export type Drill = {
  id: number
  lesson_id: number
  drill_type: string
  prompt_text: string
  base_sentence: string
  target_answer: string
  metadata_json: Record<string, unknown>
  sequence_order: number
}

export type ProgressItem = {
  lesson_id: number
  lesson_title: string
  completion_rate: number
  average_score: number
}

function getToken() {
  return localStorage.getItem('token') || ''
}

async function request<T>(path: string, init?: RequestInit, auth = false): Promise<T> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(init?.headers || {}),
  }

  if (auth) {
    headers['Authorization'] = `Bearer ${getToken()}`
  }

  const resp = await fetch(`${API_BASE}${path}`, { ...init, headers })
  if (!resp.ok) {
    const text = await resp.text()
    throw new Error(text || `Request failed: ${resp.status}`)
  }

  return resp.json() as Promise<T>
}

export async function register(email: string, password: string) {
  return request<{ access_token: string }>('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export async function login(email: string, password: string) {
  return request<{ access_token: string }>('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export async function getCourses() {
  return request<Course[]>('/api/v1/courses')
}

export async function getLesson(lessonId: number) {
  return request<Lesson>(`/api/v1/lessons/${lessonId}`)
}

export async function getLessonDrills(lessonId: number) {
  return request<Drill[]>(`/api/v1/lessons/${lessonId}/drills`)
}

export async function submitAttempt(drill_id: number, input_text: string) {
  return request<{ is_correct: boolean; score: number; feedback: Record<string, unknown> }>(
    '/api/v1/attempts',
    {
      method: 'POST',
      body: JSON.stringify({ drill_id, input_text }),
    },
    true,
  )
}

export async function getMyProgress() {
  return request<{ items: ProgressItem[] }>('/api/v1/progress/me', {}, true)
}
