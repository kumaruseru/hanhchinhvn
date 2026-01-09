import os
import glob
import json
from typing import Generator, Tuple

from .models import DivisionType, Province, District, Ward, DivisionRegistry

# Path to data directory
_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def iter_all_provinces() -> Generator[Province, None, None]:
    """
    Trả về generator duyệt qua tất cả tỉnh thành.
    
    Yields:
        Province: Đối tượng Province cho mỗi tỉnh/thành phố.
    
    Example:
        >>> for province in iter_all_provinces():
        ...     print(province.name)
    """
    for province in DivisionRegistry.get_all_provinces():
        yield province


def iter_all_districts() -> Generator[Tuple[str, District], None, None]:
    """
    Trả về generator duyệt qua tất cả quận huyện của TOÀN BỘ cả nước.
    
    Yields:
        Tuple[str, District]: Tuple gồm (mã_tỉnh_cha, District_Object)
    
    Example:
        >>> for province_code, district in iter_all_districts():
        ...     print(f"{province_code}: {district.name}")
    """
    data_dir = os.path.join(_DATA_DIR, "quan_huyen")
    json_files = glob.glob(os.path.join(data_dir, "*.json"))
    
    for file_path in sorted(json_files):
        # Lấy mã tỉnh từ tên file (vd: 01.json -> 01)
        province_code = os.path.splitext(os.path.basename(file_path))[0]
        
        with open(file_path, "r", encoding="utf-8") as f:
            districts_data = json.load(f)
            for d_data in districts_data.values():
                yield province_code, District(**d_data)


def iter_all_wards() -> Generator[Tuple[str, Ward], None, None]:
    """
    Trả về generator duyệt qua tất cả xã phường.
    
    Yields:
        Tuple[str, Ward]: Tuple gồm (mã_huyện_cha, Ward_Object)
    
    Example:
        >>> for district_code, ward in iter_all_wards():
        ...     print(f"{district_code}: {ward.name}")
    """
    data_dir = os.path.join(_DATA_DIR, "xa_phuong")
    json_files = glob.glob(os.path.join(data_dir, "*.json"))
    
    for file_path in sorted(json_files):
        # Lấy mã huyện từ tên file (vd: 001.json -> 001)
        district_code = os.path.splitext(os.path.basename(file_path))[0]
        
        with open(file_path, "r", encoding="utf-8") as f:
            wards_data = json.load(f)
            for w_data in wards_data.values():
                yield district_code, Ward(**w_data)


__all__ = [
    # Models
    "DivisionType",
    "Province", 
    "District",
    "Ward",
    # Helper functions
    "iter_all_provinces",
    "iter_all_districts", 
    "iter_all_wards",
]
