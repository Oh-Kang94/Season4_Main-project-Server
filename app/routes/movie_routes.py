from flask_restx import Resource, marshal
from ..models.ApiModel import Cast_fields,Movie_fields
from ..services.movie_service import MoiveService

def movie_routes(movie_ns):
    @movie_ns.route('/movie')
    class CreateMovie(Resource):
        @movie_ns.doc(
            description = '달에 한번 csv를 통한 영화 DB 저장.',
            responses={
            500: "Failed to create movies"
        })
        def post(self):
            # Movie 먼저 생성
            resultMovie = MoiveService.create_movie()
            
            if resultMovie:
                # Movie 생성이 성공했을 경우에만 Cast 생성
                resultCast = MoiveService.create_cast()
                    
                if resultCast:
                    return {'message': 'Movies and Cast created successfully'}, 200
                else:
                    return {'message': 'Failed to create Cast'}, 500
            else:
                return {'message': 'Failed to create Movies'}, 500

    @movie_ns.route('/')
    class ReadMovie(Resource):
        @movie_ns.doc(
            description = '영화 리스트 불러오기.',
            responses={
            500: "Failed to get movies"
        })
        def get(self):
            result = MoiveService.get_movie()
            if result:
                return {'result': result}, 200
            else:
                return {'message': 'Failed to get movies'}, 500
            
    @movie_ns.route('/<int:movie_id>')
    class ReadOneMovie(Resource):
        @movie_ns.doc(
            description = '영화 1개 불러오기.',
            responses={
            500: "Failed to get movie"
        })
        def get(self,movie_id):
            result = MoiveService.get_movie_one(movie_id)
            if result:
                return {'result': marshal(result, Movie_fields)}, 200
            else:
                return {'message': 'Failed to get movie'}, 500
            
    @movie_ns.route('/cast')
    class ReadMovie(Resource):
        @movie_ns.doc(
            description = '캐스트 리스트 불러오기.',
            responses={
            500: "Failed to get casts"
        })
        def get(self):
            result = MoiveService.get_cast()
            if result:
                return {'result': result}, 200
            else:
                return {'message': 'Failed to get casts'}, 500
    
    @movie_ns.route('/cast/<int:movie_id>')
    class ReadMovie(Resource):
        @movie_ns.doc(
            description = '캐스트 1개 불러오기.',
            responses={
            500: "Failed to get cast"
        })
        def get(self, movie_id):
            result = MoiveService.get_cast_one(movie_id)
            if result:
                return {'result': marshal(result, Cast_fields)}, 200
            else:
                return {'message': 'Failed to get cast'}, 500