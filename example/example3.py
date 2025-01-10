import hawk_python_sdk


hawk_python_sdk.init({
    'token':'eyJpbnRlZ3JhdGlvbklkIjoiY2YxYzVhZGEtNzllOC00YWQ1LWFmYTQtNGMzZjI3Y2UzNWRiIiwic2VjcmV0IjoiZjk4NTc5ZTMtNGZmMy00YmVlLThjYzEtOWVlMDY0ZjU4YTRjIn0=',
    'release': '3.12.4'
})
hawk_python_sdk.send(
    event=Exception("Something went wrong"),
    context={
        'ip': '192.168.1.1'
    },
    user={'id': 2, 'name': 'Bob'}
)
print('Event sent successfully')