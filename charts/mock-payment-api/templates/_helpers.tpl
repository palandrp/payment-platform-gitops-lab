{{- define "mock-payment-api.name" -}}mock-payment-api{{- end -}}
{{- define "mock-payment-api.labels" -}}
app.kubernetes.io/name: {{ include "mock-payment-api.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
