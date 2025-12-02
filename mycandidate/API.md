# API Documentation

## GET /api/v1/wards/<ward_id>/candidates

Returns all candidates standing for election in a specific ward.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| ward_id | string | Ward number (e.g., "1", "2") |

### Response

```json
{
  "ward": "Ward 1",
  "count": 3,
  "candidates": [
    {
      "full_names": "Steve",
      "surname": "Rogers",
      "party": "Democratic Alliance",
      "age": "36",
      "gender": "Male",
      "orderno": "1"
    }
  ]
}
```

### Error Response

If ward doesn't exist:

```json
{
  "error": "Ward not found",
  "ward_id": "99"
}
```

Status code: 404

### Example

```bash
curl http://localhost:5000/api/v1/wards/1/candidates
```
