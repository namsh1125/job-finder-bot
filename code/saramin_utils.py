def filter_and_format_location(location):
    if not location:
        return "위치 정보 없음"

    try:
        locations = location.split(',')
        grouped_locations = {}

        for loc in locations:
            # '전체'로 끝나는 경우 필터링
            if loc.endswith('전체'):
                continue

            # 지역 이름 분리 (ex: 서울 > 강남구)
            region, city = loc.split(' &gt; ')

            # 지역별로 도시 정보 그룹화
            if region in grouped_locations:
                grouped_locations[region].append(city)
            else:
                grouped_locations[region] = [city]

        # 지역별로 도시 정보 문자열로 조립
        formatted_locations = []
        for region, cities in grouped_locations.items():
            formatted_cities = ', '.join(cities)
            formatted_locations.append(f"{region} > {formatted_cities}")

        result = '\n'.join(formatted_locations)
        return result

    except (ValueError, IndexError) as e:
        raise e
