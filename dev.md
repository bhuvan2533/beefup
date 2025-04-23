# 🛠️ MVP Feature List

## ✅ Core Features

### User Authentication (Optional)
- **JWT Bearer Token**: Supports roles such as `admin` or `client`.

### Job Description Upload
- **Endpoint**: `POST /api/job-description/`

### Employee Profile Upload
- **Endpoint**: `POST /api/profile/`

### Match Percentage API
- **Endpoint**: `POST /api/match/`
- **Input**: Job Description (JD) + Profile
- **Output**: Match Percentage (%) + Summary

### Profile Enhancement API
- **Endpoint**: `POST /api/enhance/`
- **Input**: Profile + Job Description (JD)
- **Output**: Enhanced Profile